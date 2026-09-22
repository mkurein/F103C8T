# CLAUDE.md

@AGENTS.md

## Claude Code specifics

- Рабочая папка — этот репозиторий (`primGPT/`), не родительская `STM32F1/` (ADR-009).
- Общение на русском.
- Сборка из PowerShell (PATH к toolchain задаётся вручную):

```powershell
$env:PATH = "C:\ST\STM32CubeIDE_1.17.0\STM32CubeIDE\plugins\com.st.stm32cube.ide.mcu.externaltools.make.win32_2.2.0.202409170845\tools\bin;C:\ST\STM32CubeIDE_1.17.0\STM32CubeIDE\plugins\com.st.stm32cube.ide.mcu.externaltools.gnu-tools-for-stm32.13.3.rel1.win32_1.0.0.202411081344\tools\bin;$env:PATH"
make -C Debug all -j8
arm-none-eabi-size Debug/primGPT.elf
```

- Файлы проекта в CRLF — сохранять окончания строк при правках.
- Факты о проекте держать в `docs/`, не в памяти чата: изменилось — обнови doc в том же commit.
