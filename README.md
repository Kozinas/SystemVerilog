# SystemVerilog: язык, RTL и проверка проектов

Русскоязычная методичка с объяснениями, примерами и упражнениями. Начинать можно
с основ цифровой логики; опыт Verilog не требуется. Основной маршрут — синтезируемый
RTL, затем проверка и моделирование. Нормативная база — **IEEE 1800-2023**.

**[Скачать итоговый PDF](dist/systemverilog.pdf)** ·
[Единый Markdown](dist/systemverilog.md) ·
[Результаты проверок](VALIDATION.md) ·
[Примеры и запуск](examples/README.md)

Текст написан самостоятельно. [Первичный план](PLAN.md) использован как перечень
тем; [таблица соответствия](docs/appendices/d-plan-map.md) объясняет перестановки
и дополнения. Это учебный курс по всем основным областям SystemVerilog, включая
несинтезируемые средства, но не замена полной нормативной грамматике IEEE.
Сам стандарт [доступен бесплатно через IEEE GET](https://standards.ieee.org/ieee/1800/7743/).
Дата проверки источников: 23 сентября 2026 года.

## План и главы

Порядок задаёт [book.json](book.json). Каждая строка оглавления ведёт к главе;
в PDF этот же порядок используется для оглавления и закладок.

<!-- TOC:START -->

### I. Основы

- [01. Аппаратное мышление и устройство языка](docs/01-foundations/01-introduction.md)
- [02. Лексика, литералы и четыре состояния](docs/01-foundations/02-lexical.md)
- [03. Модули, порты и иерархия](docs/01-foundations/03-modules.md)
- [04. Время и планировщик симуляции](docs/01-foundations/04-simulation.md)

### II. Данные и выражения

- [05. Сети, переменные и встроенные типы](docs/02-data/05-types.md)
- [06. Операции, размер и знаковость](docs/02-data/06-expressions.md)
- [07. typedef, enum, структуры и объединения](docs/02-data/07-aggregate-types.md)
- [08. Массивы, очереди и методы](docs/02-data/08-arrays.md)
- [09. Совместимость и приведение типов](docs/02-data/09-casts.md)

### III. Конструкции языка

- [10. Присваивания и процессы RTL](docs/03-language/10-assignments.md)
- [11. Условия, выбор и циклы](docs/03-language/11-control.md)
- [12. Функции, задачи и время жизни](docs/03-language/12-subroutines.md)
- [13. Пакеты, области видимости и bind](docs/03-language/13-packages.md)
- [14. Параметры и generate](docs/03-language/14-generate.md)
- [15. Интерфейсы и modport](docs/03-language/15-interfaces.md)
- [16. Препроцессор и единицы компиляции](docs/03-language/16-preprocessor.md)

### IV. Проектирование RTL

- [17. Комбинационная логика и арифметика](docs/04-rtl/17-combinational.md)
- [18. Регистры, сброс и конвейеры](docs/04-rtl/18-sequential.md)
- [19. Память, ROM и очереди FIFO](docs/04-rtl/19-memory.md)
- [20. Конечные автоматы и протоколы](docs/04-rtl/20-fsm.md)
- [21. Тактирование, CDC и переносимость](docs/04-rtl/21-timing.md)
- [22. Сквозной проект: синхронный FIFO](docs/04-rtl/22-project.md)

### V. Проверка проектов

- [23. Тестбенчи, clocking и ввод-вывод](docs/05-verification/23-testbenches.md)
- [24. Параллельные процессы и синхронизация](docs/05-verification/24-processes.md)
- [25. Классы и объектная модель](docs/05-verification/25-classes.md)
- [26. Случайные воздействия и ограничения](docs/05-verification/26-random.md)
- [27. Assertions, sequences и properties](docs/05-verification/27-assertions.md)
- [28. Функциональное покрытие](docs/05-verification/28-coverage.md)
- [29. DPI, VPI и границы UVM](docs/05-verification/29-foreign.md)

### VI. Моделирование и инструменты

- [30. Примитивы, силы и пользовательские сети](docs/06-modeling/30-primitives.md)
- [31. specify, задержки и библиотечные модели](docs/06-modeling/31-timing-models.md)
- [32. Библиотеки и конфигурации](docs/06-modeling/32-configurations.md)
- [33. Стандарты, изменения 2023 и рабочий процесс](docs/06-modeling/33-tools-standards.md)

### Приложения

- [A. Матрица синтезируемости](docs/appendices/a-synthesis.md)
- [B. Справочник ключевых слов и системных средств](docs/appendices/b-reference.md)
- [C. Упражнения и ответы](docs/appendices/c-exercises.md)
- [D. Соответствие исходному PLAN.md](docs/appendices/d-plan-map.md)
- [E. Источники и порядок проверки фактов](docs/appendices/e-sources.md)
- [F. Словарь и предметный указатель](docs/appendices/f-index.md)
<!-- TOC:END -->

## Сборка PDF

Нужен Python 3.10 или новее. На Windows, из корня репозитория:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe tools/book.py check
.\.venv\Scripts\python.exe tools/book.py build
```

Linux/macOS:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python tools/book.py check
.venv/bin/python tools/book.py build
```

Результат — `dist/systemverilog.pdf` и `dist/systemverilog.md`. Для одной сборки
достаточно `requirements.txt`; зависимости `-dev` нужны для дополнительных проверок.
TeX, Pandoc и офисные программы не требуются. Windows: Arial и Consolas из системной
папки шрифтов. Linux: пакет `fonts-dejavu-core`. Для других систем укажите
`--font`, `--bold-font`, `--mono-font` (пути к TTF с кириллицей) после `build`.
Сборка после установки зависимостей работает без сети.

```text
python tools/book.py toc       # обновить оглавление README
python tools/check_sv.py       # компиляция автономных примеров через slang
python tools/check_pdf.py      # кириллица, заголовки, ссылки и закладки PDF
python tools/simulate.py       # тест FIFO, нужен Icarus Verilog в PATH
python -m unittest discover -s tools/tests -v
```

В Markdown главы кодовые блоки могут быть учебными фрагментами с пояснённым
контекстом. Компилируемые целые примеры хранятся в `examples`; статус компиляции
и симуляции не смешивается. Правила развития методички — в [AGENTS.md](AGENTS.md).

GitHub Actions автоматически проверяет главы и примеры, моделирует FIFO и
собирает PDF как артефакт запуска. Исходный `PLAN.md` сохраняется отдельно;
для обновления таблицы соответствия есть `python tools/map_plan.py`.
