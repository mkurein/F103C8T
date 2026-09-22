# Task template (Qwen / OpenCode)

Копировать, заполнить, отдать модели. Этап A (Plan) — без правок файлов.

```text
PROJECT:
primGPT — STM32F103C8 + FreeRTOS, UART1 command protocol (see AGENTS.md)

TASK:
<T-номер из docs/TODO.md и одна фраза>

GOAL:
<наблюдаемый результат>

CONSTRAINTS:
- Edit only inside USER CODE BEGIN/END in CubeMX files.
- Do not regenerate from primGPT.ioc (ADR-005).
- Do not change task priorities, stack sizes, heap size.
- Do not change UART1 frame format unless PROTOCOL.md is updated first.
- No HAL_Delay in tasks; no large arrays on task stacks.
- RAM 20 KB, heap 10 KB: no new dynamic allocation.

FILES:
- <file / function>

ERROR / LOG:
<последние строки UART3 или вывод make>

EXPECTED:
<что должно получиться>

BEFORE CHANGING:
Explain the cause, related functions, minimal change, side effects.

AFTER CHANGING:
Show only modified functions. Build: make -C Debug all -j8
```

После: `git --no-pager diff` → `make` → плата → `git commit`.
Сделанное отметить `[x]` в TODO.md.
