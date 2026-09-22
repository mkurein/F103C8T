# Hardware

## Board

- Blue Pill, STM32F103C8Tx (LQFP48), Cortex-M3
- HSE 8 MHz → PLL x9 → SYSCLK 72 MHz; AHB 72, APB1 36, APB2 72 MHz
- Flash 64 KB @ 0x08000000, RAM 20 KB @ 0x20000000
  (linker: `STM32F103C8TX_FLASH.ld`)
- SVD: `STM32F103.svd` (Cortex-Debug peripherals view)

## Peripherals

| Periph | Config | Used by |
|--------|--------|---------|
| USART1 | 38400 8N1, RX IT | command protocol |
| USART3 | 115200 8N1, TX polling | debug log |
| SPI1 | master, mode 0, /16 = 4.5 MHz, MSB first, soft NSS | FRAM |
| TIM1 | HAL timebase 1 kHz | `HAL_GetTick` |
| SysTick | FreeRTOS tick 1 kHz | kernel |

Пины: [PINOUT.md](PINOUT.md).

## FRAM

- 32 KB (`FRAM_MEM_SIZE` 0x8000), SPI, 16-bit address.
- Opcodes: WREN 0x06, WRDI 0x04, RDSR 0x05, WRSR 0x01, READ 0x03, WRITE 0x02.
- Модель микросхемы в проекте не записана — см. TODO.

## Debug / flash

- ST-Link V2, SWD (PA13 SWDIO, PA14 SWCLK)
- OpenOCD из STM32CubeIDE 1.17.0; конфиг `primGPT Debug.cfg`
- VS Code / Cursor: `.vscode/launch.json` (Cortex-Debug)
- Лимит: 6 аппаратных breakpoints (1 занят `runToEntryPoint`)

## Build

- Makefile генерирует STM32CubeIDE в `Debug/` (один раз собрать в IDE).
- VS Code: `Ctrl+Shift+B` → `make -C Debug all -j8`.
- Выход: `Debug/primGPT.elf`, `.bin`, `.hex`, `.map`.

Пошагово: [guides/QUICKSTART.md](guides/QUICKSTART.md).
