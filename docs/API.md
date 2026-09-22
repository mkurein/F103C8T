# API — firmware modules

Сигнатуры публичных функций, чтобы не грузить в контекст целые файлы.

## uart.h / uart.c

| Function | Notes |
|----------|-------|
| `void log_printf(const char *fmt, ...)` | UART3, buf 128 B, blocking 100 ms |
| `void printf_uart3(const char *fmt, ...)` | то же, с обрезкой длины |
| `void uart1_put_ch(char ch)` | UART1, blocking `HAL_MAX_DELAY` |
| `void uart1_put_u16(uint16_t)` / `uart1_put_u32(uint32_t)` | MSB first |
| `int uart_read(char *ch)` | из ring buffer; **не используется** |
| `char usart_recv_byte(UART_HandleTypeDef *)` | blocking RX; **не используется** |
| `void HAL_UART_RxCpltCallback(UART_HandleTypeDef *)` | ISR → `uartQueue` |
| `int _write(int, char *, int)` | newlib hook: `printf` → **UART1** |

Globals: `uart1_rx_buf[UART_BUF_SIZE]`, `uart1_rx_head`, `uart1_rx_tail`.
Extern из main.c: `uartQueue`, `last_rx_time`, `huart1`, `huart3`.

## crc16.h / crc16.c

| Function | Notes |
|----------|-------|
| `uint16_t crc16(const uint8_t *data, uint16_t len)` | CRC-16/MODBUS |
| `int process_crc(uint8_t *data, uint16_t len, bool check)` | check=true → 1 если CRC ок; false → дописать CRC LSB first, вернуть len+2 (буфер ≥ len+2) |
| `void calculate_crc_for_2_bytes(const uint8_t *in, uint8_t *out)` | out[4] = in[0..1] + CRC; реентерабельна |

## fram.h / fram.c

| Function | Notes |
|----------|-------|
| `void fram_cfg_setup(fram_cfg_t *)` | пины SPI1 + CS PA4 (баг T2) |
| `int fram_init(fram_t *, fram_cfg_t *)` | привязка к `hspi1`, CS high; 0 = ok |
| `void fram_read(fram_t *, uint16_t addr, uint8_t *buf, uint16_t n)` | |
| `void fram_write(fram_t *, uint16_t addr, uint8_t *buf, uint16_t n)` | WREN → WRITE → WRDI |
| `uint8_t fram_read_status(fram_t *)` / `void fram_write_status(fram_t *, uint8_t)` | |
| `void fram_write_enable/disable(fram_t *)` | |
| `void fram_erase_all(fram_t *)` | **опасно**: 32 KB на стеке (T3) |

Все вызовы blocking (`HAL_MAX_DELAY`), без mutex.

## DataFile.h

`UART_TIMEOUT_MS 20`, `UART_BUF_SIZE 100`, `polynomial 0xA001`,
`ID_BU 1`, `ID_BZ 2`, `ID_BF 3`.

## main.c (tasks)

`LedTask`, `Uart1Task`, `StartDefaultTask`, `vApplicationStackOverflowHook`,
`vApplicationMallocFailedHook`, `Error_Handler`. Globals: `fram`, `cfgFRAM`,
`uartQueue`, `last_rx_time`, `*TaskHandle`, `*_attributes`.
