# Pinout

Источник истины — `primGPT.ioc` (но см. ADR-005: код и .ioc расходятся).

| Pin | Function | Mode | Owner | Note |
|-----|----------|------|-------|------|
| PA4 | FRAM CS | GPIO out PP | fram.c | soft NSS, active low |
| PA5 | SPI1_SCK | AF PP | fram.c | |
| PA6 | SPI1_MISO | input | fram.c | |
| PA7 | SPI1_MOSI | AF PP | fram.c | |
| PA9 | USART1_TX | AF PP | uart.c | protocol |
| PA10 | USART1_RX | input | uart.c | protocol |
| PB10 | USART3_TX | AF PP | uart.c | debug log |
| PB11 | USART3_RX | input | — | не используется |
| PC13 | LED | GPIO out PP | LedTask, cmd 0x70 | active low |
| PC15 | activity | GPIO out PP | Uart1Task | toggle каждую итерацию |
| PA13 | SWDIO | SWD | debugger | не занимать |
| PA14 | SWCLK | SWD | debugger | не занимать |
| PD0/PD1 | HSE 8 MHz | OSC | RCC | |

Свободны: остальные PA/PB (PA0–PA3, PA8, PA11/12 = USB, PA15, PB0–PB9, PB12–PB15).
JTAG отключён (`__HAL_AFIO_REMAP_SWJ_NOJTAG` в msp), поэтому PA15/PB3/PB4 — обычные GPIO.
PC14/PC15 — выводы LSE, PC13–PC15 слаботочные (≤ 3 mA).
