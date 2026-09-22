# Safety / failure handling

Проект учебный: исполнительных механизмов нет (только LED и FRAM).
Здесь — что происходит при сбоях, чтобы новые правки это не ломали.

## Failure states

| Event | Detection | Reaction | Visible as |
|-------|-----------|----------|------------|
| HAL init error | `!= HAL_OK` в `MX_*_Init`, clock | `printf` → `Error_Handler`: IRQ off, halt | текст в UART1 (!) |
| Stack overflow | FreeRTOS method 2 | hook: log, IRQ off, halt | `!!! Stack overflow: <task>` в UART3 |
| Heap exhausted | malloc-failed hook | log, IRQ off, halt | `!!! Malloc failed` в UART3 |
| Queue create fail | `uartQueue == NULL` | `Error_Handler` | — |
| Uart1Task create fail | handle NULL | `'E'` в UART1, `Error_Handler` | `E` |
| RX overflow ring | head == tail | ring reset в 0 | нет |
| Bad CRC | `process_crc` | команда не выполняется | ответ всё равно `01 00` (T6) |
| Reset | `RCC->CSR` at boot | лог, флаги сброшены | `Rst:0x........` в UART3 |

## Not implemented

- Watchdog (IWDG / WWDG) — после halt MCU висит до ручного сброса.
- Fault handlers (HardFault и др.) — стандартные циклы CubeMX, без лога.
- Mutex на общие периферии (см. ARCHITECTURE: ownership).

## Rules for changes

- Не блокировать `Uart1Task` надолго: байты, пришедшие за это время, копятся
  в очереди (40 B, дальше теряются) и выбрасываются flush-ем после ответа.
- Любой вызов `*FromISR` — только из IRQ с приоритетом 5..15.
- Новые аварийные пути — лог в UART3, не в UART1.
