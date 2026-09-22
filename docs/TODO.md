# TODO

Одна задача = один commit. Перед задачей — анализ (Plan), потом правка (Build),
потом `make -C Debug all` и проверка на плате.

## Current

- [ ] **T1** `Uart1Task`: заменить `HAL_Delay(1000)` в cmd 0x02 на `vTaskDelay`
  (или убрать: FRAM не требует паузы после записи). Files: `main.c`.

## Next

- [ ] **T2** `fram_cfg_setup`: `sck_port` присваивается 3 раза, `miso_port` / `mosi_port`
  не заполняются. Files: `fram.c`.
- [ ] **T3** `fram_erase_all`: `uint8_t empty_data[0x8000]` на стеке (32 KB > вся RAM).
  Писать чанками из static буфера 32–64 B. Files: `fram.c`.
- [ ] **T4** `_write` (printf) идёт в UART1 = командный канал. Перенаправить в UART3.
  Files: `uart.c`. Проверить `Error_Handler`, `SystemClock_Config`.
- [ ] **T5** Cmd 0x70 перетирается `LedTask` через ≤ 1 s. Решить: LedTask мигает
  только в «авто»-режиме или LED команды → другой пин. Files: `main.c`. Сначала ADR.
- [ ] **T6** Ответ всегда `01 00` даже при ошибке CRC / неизвестной команде.
  Ввести коды ошибок. Сначала `PROTOCOL.md`.
- [ ] **T7** Результат FRAM-теста (cmd 0x02) не возвращается хосту.
  Сравнить `rd_data` с `wr_data`, вернуть статус. Сначала `PROTOCOL.md`.
- [ ] **T8** Синхронизировать `primGPT.ioc` с кодом (ADR-005): USART1_IRQn prio 5,
  USART3 без IRQ, defaultTask 1024 B, USART3 init внутри USER CODE.
- [ ] **T9** Перенести `LedTask` / `Uart1Task` / команды из `main.c` в свои модули
  (`app_led.c`, `app_uart1.c`, `commands.c`).

## Later

- [ ] Python-скрипт хоста `tools/host.py` (pyserial): отправка команд, проверка CRC,
  pytest для `crc16` на ПК.
- [ ] Unit-тест `crc16.c` на ПК (gcc host build).
- [ ] IWDG watchdog + причина сброса в лог (ADR-007 → расширить).
- [ ] Кадр с `LEN` и `REQUEST_ID` (см. guide §28), версия протокола.
- [ ] Mutex на UART3, если логировать начнёт больше одной задачи.
- [ ] Записать модель FRAM-микросхемы в `HARDWARE.md`.
- [ ] Новый замер RAM (строка v0.4 в notes/README_RAM_RTOS.md §19): bss вырос
  14644 → 16180 B, причина не выяснена.
- [ ] Убрать мёртвый код: `uart_read`, `usart_recv_byte`, закомментированные блоки.

## Done

- [x] Hooks stack overflow / malloc failed (ADR-007)
- [x] Heap 14 → 10 KB (ADR-006)
- [x] `UART_TIMEOUT_MS` 200 → 20 ms (ADR-002)
- [x] `calculate_crc_for_2_bytes` реентерабельна (буфер вызывающего)
- [x] 2026-09-22 Документация → схема `docs/` (ADR-009, ADR-010)
