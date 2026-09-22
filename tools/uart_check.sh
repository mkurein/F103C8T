#!/usr/bin/env bash
# primGPT: send FRAM test command 02 00 to UART1 and measure its effect on the UART3 log.
# Run in Git Bash (not WSL):  ./uart_check.sh [CMD_PORT] [LOG_PORT]
# Double-click uart_check_sh.bat, not this .sh (Windows opens .sh in a blank window).
# Defaults: CMD_PORT=COM3 (UART1, 38400), LOG_PORT=COM5 (UART3, 115200)

CMD_PORT=${1:-COM3}
LOG_PORT=${2:-COM5}

python - "$CMD_PORT" "$LOG_PORT" <<'EOF'
import sys, time, re
import serial

def say(msg):
    print(msg, flush=True)

cmd_port, log_port = sys.argv[1], sys.argv[2]
frame = bytes.fromhex('02 00 00 D0')
say(f'Команда: 02 00   кадр на провод: {frame.hex(" ")}')
say(f'UART1 {cmd_port} 38400 (команда), UART3 {log_port} 115200 (лог)')
say('Открываю порты...')
try:
    log = serial.Serial(log_port, 115200, timeout=0.1)
    cmd = serial.Serial(cmd_port, 38400, timeout=3)
except serial.SerialException as e:
    sys.exit(f"Port error: {e}\nПорт занят другой программой или переходник не подключён.")

# Sync to a Tick line and send 900 ms later, just before defaultTask wakes again:
# a blocking command then delays the next Tick by ~930 ms every time.
say('Жду строку Tick: в UART3 (до 3 с)...')
log.reset_input_buffer(); buf = b''
t = time.time()
while b'Tick:' not in buf and time.time() - t < 3: buf += log.readline()
if b'Tick:' not in buf:
    sys.exit(f"No Tick lines on {log_port}: wrong port or board is not running.")
say('Tick есть. Пауза 900 ms — шлём чуть до следующего Tick...')
time.sleep(0.9)
say(f'Отправляю {frame.hex(" ")} в {cmd_port}, жду ответ 4 байта (до 3 с)...')
t0 = time.time(); cmd.write(frame)
reply = cmd.read(4); dt = (time.time() - t0) * 1000
say(f'Ответ: {reply.hex(" ") or "(нет)"}. Читаю лог UART3 ещё 3.5 с...')
t = time.time()
while time.time() - t < 3.5: buf += log.read(256)
log.close(); cmd.close()
say('Готово.\n')

ticks = [int(x) for x in re.findall(rb'Tick:(\d+)', buf)]
steps = [b - a for a, b in zip(ticks, ticks[1:])]
stalls = [s for s in steps if s > 1100]
print('reply:', reply.hex(' ') or '(нет ответа)', f'after {dt:.0f} ms')
print('Tick steps, ms:', steps)
print('tasks stalled:', f'YES, max step {max(stalls)} ms' if stalls else 'no')
EOF
