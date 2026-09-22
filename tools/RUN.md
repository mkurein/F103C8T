# tools — запуск на Windows (PowerShell)

Оба скрипта запускаются из PowerShell. Они шлют кадр на **UART1** (38400)
и читают лог **UART3** (115200): ответ с CRC и шаг между строками `Tick:`.

| Файл | Из PowerShell | Команда |
|------|----------------|---------|
| [`uart_check.py`](uart_check.py) | напрямую | любая: `02 00`, `70 01`, … |
| [`uart_check.sh`](uart_check.sh) | через `bash.exe` | только FRAM-тест `02 00 00 D0` |
| [`uart_check.bat`](uart_check.bat) | двойной щелчок | Python, `02 00` (или аргументы, как у `.py`) |
| [`uart_check_sh.bat`](uart_check_sh.bat) | двойной щелчок | Git Bash + `.sh`, только `02 00` |

Протокол: [`docs/PROTOCOL.md`](../docs/PROTOCOL.md).

Копии на рабочем столе и в `tools\` — одни и те же скрипты. Ниже пути
на рабочий стол, как при проверке; для репозитория замените папку на
`C:\Project\ProjectSTM32\STM32F1\primGPT\tools`.

## Что нужно

1. Плата прошита: в UART3 раз в секунду идёт `Tick:<ms>`.
2. Два USB–TTL: UART1 TX/RX 38400, UART3 TX платы → RX ПК 115200.
3. Python 3 + `pyserial` (`python -m pip install pyserial`).
4. Git for Windows, если запускаете `.sh`
   (`C:\Program Files\Git\bin\bash.exe`).
5. Порты свободны (не открыты в PuTTY / Serial Monitor).

Порты по умолчанию: **COM3** = UART1, **COM5** = UART3.

```powershell
Get-CimInstance Win32_SerialPort | Select-Object DeviceID, Name, Description
```

Не WSL: там порты выглядят как `/dev/ttyS*`, а скрипты ждут `COM3` / `COM5`.

## Синхронизация с Tick

Раньше кадр уходил в случайный момент относительно `defaultTask`.
Провал Tick тогда получался от 0 до 1000 ms — один прогон на старой
прошивке мог показать `stalled: no`.

Сейчас оба скрипта (и печатают каждый шаг, пауза до ответа ~8 с):

1. ждут строку `Tick:` в UART3 (таймаут 3 s);
2. спят 900 ms (чуть до следующего пробуждения `defaultTask`);
3. шлют команду и ещё ~3.5 s читают лог.

На старой прошивке (`HAL_Delay(1000)` в cmd `0x02`) результат стабилен.
Пять прогонов подряд:

```text
reply: 01 00 00 20 after 1028 ms
Tick steps, ms: [1931, 1000, 1001, 1012]
tasks stalled: YES, max step 1931 ms
```

`tasks stalled: YES` — шаг между двумя `Tick:` больше 1100 ms
(дефект T1 в `docs/TODO.md`). После замены `HAL_Delay` на `vTaskDelay`
ожидается `stalled: no` и шаги около 1000 ms.

## `uart_check.py`

CRC16-MODBUS дописывается сам — в аргументах только байты команды.

С рабочего стола:

```powershell
python "$([Environment]::GetFolderPath('Desktop'))\uart_check.py"
python "$([Environment]::GetFolderPath('Desktop'))\uart_check.py" 70 01
python "$([Environment]::GetFolderPath('Desktop'))\uart_check.py" 70 00
python "$([Environment]::GetFolderPath('Desktop'))\uart_check.py" 02 00 --cmd COM3 --log COM5
```

Из `tools\`:

```powershell
cd C:\Project\ProjectSTM32\STM32F1\primGPT\tools
python .\uart_check.py
python .\uart_check.py 70 01
python .\uart_check.py 02 00 --cmd COM3 --log COM5
```

Двойной щелчок — по [`uart_check.bat`](uart_check.bat), не по `.py` и не
по `RUN.md` (браузер / редактор, пустое окно).

| Байты | Смысл | Кадр на проводе |
|-------|--------|-----------------|
| `02 00` | тест FRAM | `02 00 00 D0` |
| `70 01` | LED on (PC13) | `70 01 E5 B0` |
| `70 00` | LED off | `70 00 24 70` |

`uart_check.py` ещё печатает `sent:` и `reply CRC:`. Норма ответа —
`01 00 00 20`, CRC `OK`.

## `uart_check.sh`

Шлёт только `02 00 00 D0`. Двойной щелчок по `.sh` на Windows даёт
пустое окно — щёлкайте [`uart_check_sh.bat`](uart_check_sh.bat)
(лежит рядом с `.sh`, в том числе на рабочем столе).

Из PowerShell вызывайте Git Bash по полному пути (не `.\uart_check.sh`
и не WSL).

Рабочий стол:

```powershell
& "C:\Program Files\Git\bin\bash.exe" "$([Environment]::GetFolderPath('Desktop'))\uart_check.sh"
& "C:\Program Files\Git\bin\bash.exe" "$([Environment]::GetFolderPath('Desktop'))\uart_check.sh" COM3 COM5
```

Репозиторий:

```powershell
& "C:\Program Files\Git\bin\bash.exe" "C:\Project\ProjectSTM32\STM32F1\primGPT\tools\uart_check.sh"
& "C:\Program Files\Git\bin\bash.exe" "C:\Project\ProjectSTM32\STM32F1\primGPT\tools\uart_check.sh" COM3 COM5
```

В окне самого Git Bash:

```bash
cd /c/Users/$USER/Desktop
./uart_check.sh
./uart_check.sh COM3 COM5
```

## Частые ошибки

| Сообщение | Что сделать |
|-----------|-------------|
| `Ошибка порта` / `Access is denied` | закрыть терминал на этом COM |
| `Нет строк Tick` / `No Tick lines` | не тот лог-порт, плата не запущена |
| `(нет ответа)` / `reply CRC: BAD` | не тот `--cmd`, TX/RX, baud |
| `No module named 'serial'` | `python -m pip install pyserial` |
| `bash.exe` не найден | установить Git for Windows |
| пустое окно по двойному щелчку | это `.md` / `.py` / `.sh` — нужен `.bat` |

Пока скрипт открыт, тот же COM нельзя открыть во втором терминале.
