# primGPT — STM32F103 command controller

## Goal

Учебно-пробный firmware: принимать бинарные команды по UART1 (CRC16),
управлять GPIO и SPI FRAM, писать диагностику RTOS в UART3.
Полигон для приёмов, которые потом пойдут в большие проекты
(теплица на H743ZI2 и др.).

## Hardware

- MCU: STM32F103C8Tx (Blue Pill), Cortex-M3, 72 MHz
- Flash 64 KB, RAM 20 KB
- SPI FRAM 32 KB
- Debug: ST-Link V2, SWD, OpenOCD

Подробно: [HARDWARE.md](HARDWARE.md), [PINOUT.md](PINOUT.md).

## Software

- STM32 HAL (CubeMX-generated init), C11
- FreeRTOS v10.0.1, CMSIS-RTOS v2 wrapper, heap_4
- Toolchain: STM32CubeIDE 1.17.0, GCC 13.3, newlib-nano
- Editors: VS Code / Cursor (Cortex-Debug), OpenCode + Qwen3.8-27B

## Communication

| Link  | Baud   | Role                              |
|-------|--------|-----------------------------------|
| UART1 | 38400  | command protocol, CRC16-MODBUS    |
| UART3 | 115200 | debug log (TX only)               |

Протокол: [PROTOCOL.md](PROTOCOL.md).

## Status (2026-09-22)

- Сборка проходит: Flash 32 860 B of 64 KB, RAM static 16 288 of 20 480 B (80 %).
- Работает: приём кадров по таймауту, CRC, команды `0x70` / `0x02`,
  диагностика heap/stack каждые 5 s.
- Известные дефекты и план: [TODO.md](TODO.md).

## Current phase

Восстановление проекта после перерыва: документация приведена
к схеме `docs/`, дальше — исправление дефектов из `TODO.md`
маленькими задачами (одна задача = один commit).

## Next task

См. раздел `Current` в [TODO.md](TODO.md).
