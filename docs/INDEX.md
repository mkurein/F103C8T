# Project Index

Сначала карта, потом только нужные файлы. `tok` — токены Qwen3.8-27B
(замер `/tokenize`, 2026-09-22). Бюджет входа ~6000 из 8192.

## Core docs (read first)

| File | tok | What |
|------|------|------|
| [PROJECT.md](PROJECT.md) | 540 | что за проект, статус |
| [ARCHITECTURE.md](ARCHITECTURE.md) | 740 | слои, модули, поток RX, ownership |
| [FREERTOS.md](FREERTOS.md) | 880 | задачи, очередь, NVIC, память |
| [PROTOCOL.md](PROTOCOL.md) | 750 | кадр UART1, CRC, команды, ответы |
| [HARDWARE.md](HARDWARE.md) · [PINOUT.md](PINOUT.md) | 590 · 420 | плата, периферия, пины |
| [API.md](API.md) | 810 | сигнатуры функций модулей |
| [SAFETY.md](SAFETY.md) | 470 | аварийные состояния |
| [DECISIONS.md](DECISIONS.md) | 930 | ADR-001..010 |
| [TODO.md](TODO.md) | 900 | задачи T1..T9 |
| [TASK_TEMPLATE.md](TASK_TEMPLATE.md) | 320 | формат задачи для Qwen |

## Source

| Area | Files | tok |
|------|-------|------|
| Tasks, init, commands | `Core/Src/main.c` (USER CODE 0, 2, 4, 5) | 5300 целиком — давать функциями |
| UART | `Core/Src/uart.c`, `Core/Inc/uart.h` | 1610 |
| FRAM | `Core/Src/fram.c`, `Core/Inc/fram.h` | 1500 |
| CRC | `Core/Src/crc16.c`, `Core/Inc/crc16.h` | 570 |
| Constants | `Core/Inc/DataFile.h` | 85 |
| RTOS config | `Core/Inc/FreeRTOSConfig.h` (нужны строки 55–157) | 1560 |
| Pin mux, NVIC | `Core/Src/stm32f1xx_hal_msp.c` | 1840 |
| IRQ handlers | `Core/Src/stm32f1xx_it.c` | 1190 |
| CubeMX | `primGPT.ioc` | 2250 |

Не грузить: `Drivers/`, `Middlewares/`, `Debug/`, `STM32F103.svd`, `.metadata`.

## Context sets (§10 Context on Demand)

| Task | Load |
|------|------|
| команда UART1 | PROTOCOL, ARCHITECTURE, `Uart1Task` из main.c, DataFile.h, crc16.h |
| приём / ISR | ARCHITECTURE, FREERTOS, uart.c, `Uart1Task` |
| FRAM | HARDWARE, API (fram), fram.c, fram.h |
| задачи / стек / heap | FREERTOS, `main()` + task bodies, FreeRTOSConfig.h (фрагмент) |
| пины / периферия | PINOUT, HARDWARE, msp.c (фрагмент), `MX_*_Init` |
| CubeMX regen | DECISIONS (ADR-005), primGPT.ioc, msp.c |

Поиск: `rg "Uart1Task" Core/`, `rg "UART_TIMEOUT_MS" .`

## Human docs (RU, long — not for LLM context)

От 1400 до 10000 tok каждый (DEBUG_GUIDE ≈ 10000 > всего окна).

| Folder | Content |
|--------|---------|
| [guides/](guides/) | QUICKSTART, VS Code (macOS / Windows), Cursor + OpenOCD, DEBUG_GUIDE, RTOS views |
| [notes/](notes/) | BOOT_ALGORITHM, README_UART (таймаут), README_RAM_RTOS (память), README_INTERRUPTS |
| [lessons/](lessons/) | мини-уроки 01–06, PROJECT_FIRMWARE_LESSON |

Если модели нужен кусок оттуда — давать раздел, не файл целиком.
