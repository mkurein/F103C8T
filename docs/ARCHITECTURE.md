# Architecture

## Layers

```text
Host (PC / Python script)
 ↓ UART1 38400, frame + CRC16
USART1 ISR  (uart.c: HAL_UART_RxCpltCallback)
 ↓ uartQueue (40 x char)
Uart1Task   (main.c)  — frame assembly, CRC check, dispatch
 ↓
Drivers     (fram.c, HAL_GPIO)
 ↓
Hardware    (PC13 LED, SPI1 FRAM)

defaultTask → UART3 log (heap/stack diagnostics)
LedTask     → PC13 toggle
```

## Modules

| File | Responsibility | Owns |
|------|----------------|------|
| `Core/Src/main.c` | init, task bodies, command dispatch | tasks, `uartQueue`, `fram` |
| `Core/Src/uart.c` | UART TX helpers, RX ISR callback, log printf | `uart1_rx_buf`, ring head/tail |
| `Core/Src/fram.c` | SPI FRAM driver, soft CS | — (uses `hspi1`) |
| `Core/Src/crc16.c` | CRC16-MODBUS | — |
| `Core/Inc/DataFile.h` | protocol constants, device IDs | — |
| `Core/Inc/FreeRTOSConfig.h` | RTOS config | — |
| `Core/Src/stm32f1xx_hal_msp.c` | pin mux, NVIC for peripherals | — |

Публичные функции модулей: [API.md](API.md).

## RX data flow (UART1)

```text
byte on PA10
 → USART1_IRQHandler → HAL_UART_IRQHandler
 → HAL_UART_RxCpltCallback:
     ring head++ ; xQueueSendFromISR(uartQueue) ;
     last_rx_time = tick ; HAL_UART_Receive_IT (re-arm, 1 byte)
 → Uart1Task:
     xQueueReceive (2 ms) → command[index++]
     if silence > UART_TIMEOUT_MS (20 ms):
         process_crc() → switch(command[0]) → reply 4 bytes
         flush queue, index = 0
```

Кольцевой буфер `uart1_rx_buf` сейчас служит только целью для
`HAL_UART_Receive_IT`; данные в задачу идут через очередь.

## Peripheral ownership

| Resource | Writer(s) | Note |
|----------|-----------|------|
| UART1 TX | Uart1Task, `_write` (printf), Error_Handler | printf идёт в командный канал |
| UART3 TX | defaultTask, `main()` до старта планировщика, hooks | без mutex: пишет одна задача |
| SPI1 / FRAM | Uart1Task | без mutex |
| PC13 | LedTask, Uart1Task (cmd 0x70) | конфликт, см. TODO |
| PC15 | Uart1Task | activity toggle |

## Rules

- Новый код — в свои модули (`Core/Src/*.c`), не в `main.c`.
- В CubeMX-файлах правки только внутри `USER CODE BEGIN/END`.
- ISR только кладёт данные в очередь; логика — в задачах.
- RTOS-структура: [FREERTOS.md](FREERTOS.md). Решения: [DECISIONS.md](DECISIONS.md).
