"""primGPT: send a command to UART1 and measure its effect on the UART3 log.

Usage:
  python uart_check.py                  -> 02 00 (FRAM test)
  python uart_check.py 70 01            -> LED on
  python uart_check.py 02 00 --cmd COM3 --log COM5

CRC16-MODBUS is appended automatically (give the command without CRC).
Double-click uart_check.bat, not this .py and not RUN.md.
"""
import argparse
import ctypes
import re
import sys
import time

import serial


def crc16(data):
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            crc = (crc >> 1) ^ 0xA001 if crc & 1 else crc >> 1
    return crc


def say(msg):
    print(msg, flush=True)


def read_for(port, seconds):
    buf = b''
    end = time.time() + seconds
    while time.time() < end:
        buf += port.read(256)
    return buf


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('frame', nargs='*', default=['02', '00'],
                   help='command bytes in hex, without CRC (default: 02 00)')
    p.add_argument('--cmd', default='COM3', help='UART1 port, 38400 (default COM3)')
    p.add_argument('--log', default='COM5', help='UART3 port, 115200 (default COM5)')
    args = p.parse_args()

    try:
        body = bytes.fromhex(''.join(args.frame))
    except ValueError:
        print('Команда должна быть в hex, например: 70 01')
        return 2
    c = crc16(body)
    frame = body + bytes([c & 0xFF, c >> 8])

    say(f'Команда: {body.hex(" ")}   кадр на провод: {frame.hex(" ")}')
    say(f'UART1 {args.cmd} 38400 (команда), UART3 {args.log} 115200 (лог)')
    say('Открываю порты...')
    try:
        log = serial.Serial(args.log, 115200, timeout=0.1)
        cmd = serial.Serial(args.cmd, 38400, timeout=3)
    except serial.SerialException as e:
        print('Ошибка порта:', e)
        print('Порт занят другой программой (PuTTY, терминал) или переходник не подключён.')
        return 1

    # Sync to a Tick line and send 900 ms later, just before defaultTask wakes again:
    # a blocking command then delays the next Tick by ~930 ms every time.
    say('Жду строку Tick: в UART3 (до 3 с)...')
    log.reset_input_buffer()
    buf = b''
    end = time.time() + 3
    while b'Tick:' not in buf and time.time() < end:
        buf += log.readline()
    if b'Tick:' not in buf:
        print(f'Нет строк Tick на {args.log}: не тот порт или плата не работает.')
        return 1
    say('Tick есть. Пауза 900 ms — шлём чуть до следующего Tick...')
    time.sleep(0.9)
    say(f'Отправляю {frame.hex(" ")} в {args.cmd}, жду ответ 4 байта (до 3 с)...')
    t0 = time.time()
    cmd.write(frame)
    reply = cmd.read(4)
    dt = (time.time() - t0) * 1000
    say(f'Ответ: {reply.hex(" ") or "(нет)"}. Читаю лог UART3 ещё 3.5 с...')
    buf += read_for(log, 3.5)
    log.close()
    cmd.close()
    say('Готово.\n')

    ticks = [int(x) for x in re.findall(rb'Tick:(\d+)', buf)]
    steps = [b - a for a, b in zip(ticks, ticks[1:])]
    stalls = [s for s in steps if s > 1100]
    crc_ok = len(reply) == 4 and crc16(reply) == 0

    print('sent:          ', frame.hex(' '))
    print('reply:         ', reply.hex(' ') or '(нет ответа)', f'after {dt:.0f} ms')
    print('reply CRC:     ', 'OK' if crc_ok else 'BAD')
    print('Tick steps, ms:', steps)
    print('tasks stalled: ', f'YES, max step {max(stalls)} ms' if stalls else 'no')
    return 0


if __name__ == '__main__':
    rc = main()
    # Started by double-click: python is the only process in its console.
    if ctypes.windll.kernel32.GetConsoleProcessList((ctypes.c_uint * 4)(), 4) == 1:
        try:
            input('\nEnter — закрыть')
        except EOFError:
            pass
    sys.exit(rc)
