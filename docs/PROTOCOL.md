# Protocol — UART1

Physical: USART1, PA9 TX / PA10 RX, 38400 8N1, no flow control.
Если меняешь протокол — сначала этот документ, потом код.

## Request frame

```text
CMD | ARG | ... | CRC_L | CRC_H
```

- Нет header, length, version, request_id.
- Конец кадра = тишина > `UART_TIMEOUT_MS` (20 ms, `DataFile.h`).
- Max длина `UART_BUF_SIZE` = 100 B; лишние байты отбрасываются.

## CRC

CRC-16/MODBUS: poly 0xA001 (reflected 0x8005), init 0xFFFF, no final XOR.
Передаётся LSB first. Проверка: CRC всего кадра вместе с CRC == 0
(`process_crc(data, len, true)` → 1). Эталон: `"123456789"` → 0x4B37.

## Commands

| CMD | ARG | Action |
|-----|-----|--------|
| 0x70 | 0x00 | PC13 = SET (LED off, Blue Pill LED active-low) |
| 0x70 | 0x01 | PC13 = RESET (LED on) |
| 0x02 | 0x00 | FRAM test: write `"KUREIN\0"` @ 0x0150, `HAL_Delay(1000)`, read back |

Другие ARG и неизвестные CMD — игнорируются. Результат FRAM-теста
наружу не передаётся.

## Response

Всегда 4 байта после **любого** кадра (даже при ошибке CRC):

```text
ID_BU (0x01) | 0x00 | CRC_L | CRC_H
```

Кодов ошибок нет. Устройство: `ID_BU=1`, `ID_BZ=2`, `ID_BF=3` (`DataFile.h`).

## Examples (hex)

| Frame | Meaning |
|-------|---------|
| `70 01 E5 B0` | LED on |
| `70 00 24 70` | LED off |
| `02 00 00 D0` | FRAM test |
| `01 00 00 20` | response OK |

## Other bytes on UART1

- `'S'` (0x53) один раз при старте `Uart1Task`.
- `printf()` идёт в UART1 через `_write` (uart.c): сообщения
  `SystemClock_Config`, `MX_*_Init`, `Error_Handler` попадают в командный
  канал. См. TODO.

## UART3 log (115200, TX only)

`Rst:0x<CSR>` → `Main started, time: <ms> ms` → `Default Task running...` →
`Tick:<ms>` каждую 1 s, + 4 строки диагностики каждые 5 s.
Аварии: `!!! Stack overflow: <task>`, `!!! Malloc failed`.

Теория таймаута кадра: [notes/README_UART.md](notes/README_UART.md).
