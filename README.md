# primGPT (F103C8T)

Firmware для STM32F103C8 (Blue Pill) на FreeRTOS: бинарные команды
по UART1 с CRC16, SPI FRAM, диагностика памяти RTOS в UART3.

## Быстрый старт

1. Один раз собрать проект в STM32CubeIDE 1.17.0 (создаётся `Debug/makefile`).
2. Открыть **эту папку** в VS Code / Cursor.
3. `Ctrl+Shift+B` — сборка, `F5` — отладка через ST-Link.

Подробно: [docs/guides/QUICKSTART.md](docs/guides/QUICKSTART.md).

## Документация

| Start here | |
|---|---|
| [docs/PROJECT.md](docs/PROJECT.md) | что за проект и в каком состоянии |
| [docs/INDEX.md](docs/INDEX.md) | карта всей документации и кода |
| [docs/TODO.md](docs/TODO.md) | что делать дальше |
| [AGENTS.md](AGENTS.md) | правила для AI-агентов (OpenCode, Claude Code) |

## Структура

```text
Core/            исходники (main.c, uart.c, fram.c, crc16.c)
Drivers/         STM32 HAL + CMSIS
Middlewares/     FreeRTOS 10.0.1
docs/            ядро документации (короткое) + guides/ notes/ lessons/
primGPT.ioc      CubeMX (см. ADR-005 перед генерацией)
```
