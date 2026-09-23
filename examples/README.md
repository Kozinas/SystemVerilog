# Примеры SystemVerilog

| Файлы | Назначение | Режим |
| --- | --- | --- |
| [rtl/sync_fifo.sv](rtl/sync_fifo.sv), [tb/tb_fifo.sv](tb/tb_fifo.sv) | FIFO и самопроверяющийся тест для глубин 1, 3, 8 | SV-2017; для Icarus `-g2012` |
| [language/core.sv](language/core.sv) | Пакет, enum, cast, packed-структура, арифметика, методы массива | SV-2017 |
| [language/verification.sv](language/verification.sv) | Классы, random, mailbox, clocking, SVA, covergroup | SV-2017, нужен поддерживающий симулятор |
| [language/primitives.sv](language/primitives.sv) | UDP и specify | SV-2017 |
| [language/sv2023.sv](language/sv2023.sv) | Soft packed union, ref static, многострочная строка | SV-2023 |

Проверка семантики всех групп (из корня, Python с requirements-dev):

```text
python tools/check_sv.py
```

Компилятор slang не выполняет симуляцию. Реальные результаты перечислены
в [VALIDATION.md](../VALIDATION.md). Файлы разных групп с отдельными top не нужно
подавать в один общий запуск симуляции.

FIFO с Icarus Verilog (команды одинаковы после установки исполняемых файлов в PATH):

```text
iverilog -g2012 -s tb_fifo -o build/fifo.vvp examples/rtl/sync_fifo.sv examples/tb/tb_fifo.sv
vvp build/fifo.vvp
```

Предварительно создайте папку `build`. Автоматически это делает:

```text
python tools/simulate.py
```

Успешный прогон обязан вывести три `PASS FIFO` и `PASS ALL FIFO CASES`.
Скрипт проверяет код возврата и наличие итогового маркера; отсутствие инструмента
или тайм-аут считаются ошибкой, а не пропуском с успешным статусом.
Для переносного Icarus вне PATH можно задать `--iverilog` и `--vvp`.
Тест меняет воздействия на negedge и проверяет обновлённое состояние после NBA;
он соблюдает удержание неподтверждённой входной транзакции.
