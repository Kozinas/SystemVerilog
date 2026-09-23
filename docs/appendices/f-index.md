# F. Словарь и предметный указатель

## Словарь

| Термин | Значение |
| --- | --- |
| HDL | Язык описания аппаратуры |
| RTL | Представление передачи и обработки данных между регистрами |
| DUT | Проверяемое устройство |
| Testbench | Окружение стимулов, наблюдения и проверок |
| Elaboration / элаборация | Построение иерархии с параметрами до моделирования |
| Driver | Источник значения сети; в тестбенче также компонент подачи стимулов |
| Net / сеть | Объект, получающий значение от драйверов по правилам разрешения |
| Variable / переменная | Объект, сохраняющий последнее присвоенное значение |
| Packed | Единое битовое представление агрегата |
| Unpacked | Агрегат самостоятельных элементов |
| Handle | Ссылка на программный объект или ресурс |
| Scope | Область видимости имени |
| Lifetime | Время существования объекта |
| NBA | Очередь неблокирующих обновлений |
| Latch | Защёлка, прозрачная при активном уровне управления |
| Flip-flop | Триггер, обновляемый по событию фронта |
| CDC / RDC | Пересечение тактовых доменов / доменов сброса |
| STA | Статический временной анализ |
| Latency | Задержка от принятия входа до соответствующего выхода |
| Throughput | Установившаяся пропускная способность |
| Backpressure | Приостановка источника неготовностью потребителя |
| Scoreboard | Проверка наблюдаемых транзакций по эталонной модели |
| Assertion | Исполняемое утверждение о поведении |
| Vacuity | Успех требования без активации существенной предпосылки |
| Coverage | Измерение наблюдённых запланированных ситуаций |
| Seed | Начальное состояние генератора случайности |
| LRM | Нормативное описание языка |
| DPI / VPI | Прямой интерфейс подпрограмм / программный доступ к объектам модели |

## Указатель по задачам

| Искомая тема | Где читать |
| --- | --- |
| Четыре состояния, числа, строки, идентификаторы | [02](../01-foundations/02-lexical.md) |
| Модуль, порт, `.name`, `.*`, alias | [03](../01-foundations/03-modules.md) |
| Время, Active/NBA, гонки | [04](../01-foundations/04-simulation.md) |
| wire, logic, bit, signed, const | [05](../02-data/05-types.md) |
| Переполнение, операторы, inside, let, streaming | [06](../02-data/06-expressions.md) |
| Enum, struct, union, assignment pattern | [07](../02-data/07-aggregate-types.md) |
| Массив, queue, associative, foreach, sum | [08](../02-data/08-arrays.md) |
| Cast, `$cast`, `$signed`, bit-stream | [09](../02-data/09-casts.md) |
| assign, `=`, `<=`, always_comb/ff/latch | [10](../03-language/10-assignments.md) |
| if, case, unique, priority, циклы | [11](../03-language/11-control.md) |
| function/task, ref, automatic/static | [12](../03-language/12-subroutines.md) |
| Package, import/export, scope, bind | [13](../03-language/13-packages.md) |
| Параметры, generate, genvar, `$clog2` | [14](../03-language/14-generate.md) |
| Interface, modport, virtual interface | [15](../03-language/15-interfaces.md) |
| Макросы, include, directives, compilation unit | [16](../03-language/16-preprocessor.md) |
| Мультиплексор, арифметика, fixed point | [17](../04-rtl/17-combinational.md) |
| Регистр, reset, enable, pipeline | [18](../04-rtl/18-sequential.md) |
| RAM/ROM, read-during-write, FIFO | [19](../04-rtl/19-memory.md), [22](../04-rtl/22-project.md) |
| FSM, Moore/Mealy, handshake | [20](../04-rtl/20-fsm.md) |
| Синхронизатор, CDC, timing constraints | [21](../04-rtl/21-timing.md) |
| Тестбенч, clocking, файлы, plusargs | [23](../05-verification/23-testbenches.md) |
| Fork, event, mailbox, semaphore, process | [24](../05-verification/24-processes.md) |
| Class, inheritance, constructor, copy | [25](../05-verification/25-classes.md) |
| Random, constraint, dist, randcase, randsequence | [26](../05-verification/26-random.md) |
| SVA, sequence, property, sampled values | [27](../05-verification/27-assertions.md) |
| Covergroup, bins, cross, functional coverage | [28](../05-verification/28-coverage.md) |
| DPI-C, VPI, UVM | [29](../05-verification/29-foreign.md) |
| UDP, силы драйверов, MOS, nettype | [30](../06-modeling/30-primitives.md) |
| Specify, SDF, timing checks | [31](../06-modeling/31-timing-models.md) |
| Config, library, extern | [32](../06-modeling/32-configurations.md) |
| IEEE 1800-2023, инструменты | [33](../06-modeling/33-tools-standards.md) |

## Указатель полных примеров

Компилируемые примеры и команды собраны в [examples/README.md](../../examples/README.md).
Сквозной FIFO соединяет темы глав 03–22. `core.sv` проверяет типы и выражения,
`verification.sv` демонстрирует проверочную модель, `primitives.sv` — UDP/specify,
`sv2023.sv` — отдельные дополнения новой редакции. Фактический статус каждого
набора проверок — [VALIDATION.md](../../VALIDATION.md).
