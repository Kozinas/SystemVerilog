# B. Справочник ключевых слов и системных средств

Ключевые слова чувствительны к регистру и пишутся строчными буквами.
Ни `$display`, ни `randomize`, ни `uvm_component` не являются зарезервированными
ключевыми словами только потому, что часто встречаются в SV-коде.
Режим `` `begin_keywords `` может менять набор распознаваемых слов.

## Алфавитный указатель ключевых слов

Ниже объединённый словарь языка, включая прежние средства Verilog и
специализированные временные конструкции. Смысл слова определяется контекстом:
`and` бывает вентилем и оператором последовательностей; `static` — lifetime
и член класса; `soft` — ограничение или разновидность объединения.

```text
accept_on alias always always_comb always_ff always_latch and assert assign
assume automatic before begin bind bins binsof bit break buf bufif0 bufif1
byte case casex casez cell chandle checker class clocking cmos config const
constraint context continue cover covergroup coverpoint cross deassign
default defparam design disable dist do edge else end endcase endchecker
endclass endclocking endconfig endfunction endgenerate endgroup endinterface
endmodule endpackage endprimitive endprogram endproperty endsequence
endspecify endtable endtask enum event eventually expect export extends
extern final first_match for force foreach forever fork forkjoin function
generate genvar global highz0 highz1 if iff ifnone ignore_bins illegal_bins
implements implies import incdir include initial inout input inside instance int
integer interconnect interface intersect join join_any join_none large let
liblist library local localparam logic longint macromodule matches medium
modport module nand negedge nettype new nexttime nmos nor noshowcancelled not notif0
notif1 null or output package packed parameter pmos posedge primitive
priority program property protected pull0 pull1 pulldown pullup
pulsestyle_ondetect pulsestyle_onevent pure rand
randc randcase randsequence rcmos real realtime ref reg reject_on release
repeat restrict return rnmos rpmos rtran rtranif0 rtranif1 s_always
s_eventually s_nexttime s_until s_until_with scalared sequence shortint
shortreal showcancelled signed small soft solve specify specparam static
string strong strong0 strong1 struct super supply0 supply1 sync_accept_on
sync_reject_on table tagged task this throughout time timeprecision timeunit
tran tranif0 tranif1 tri tri0 tri1 triand trior trireg type typedef union
unique unique0 unsigned until until_with untyped use uwire var vectored
virtual void wait wait_order wand weak weak0 weak1 while wildcard wire with
within wor xnor xor
```

Это навигационный список, не грамматика допустимых сочетаний. Полный
нормативный словарь и продукционные правила находятся в приложениях IEEE 1800.
Новые роли слов в 2023 не обязательно добавляют новое зарезервированное слово.

## Системные задачи и функции по назначению

| Задача | Основные средства | Замечание |
| --- | --- | --- |
| Печать | `$display`, `$write`, `$strobe`, `$monitor`, `$monitoron`, `$monitoroff` | Разный момент/условия печати |
| Ошибка и завершение | `$info`, `$warning`, `$error`, `$fatal`, `$finish`, `$stop`, `$exit` | Код возврата зависит и от flow |
| Форматирование | `$sformat`, `$sformatf`, `$swrite` | Строка, а не обязательно вывод в консоль |
| Файлы | `$fopen`, `$fclose`, `$fdisplay`, `$fwrite`, `$fgets`, `$fscanf`, `$sscanf` | Проверять статус |
| Доступ к файлу | `$fgetc`, `$ungetc`, `$fread`, `$feof`, `$ferror`, `$fflush`, `$fseek`, `$ftell`, `$rewind` | EOF не заменяет проверку чтения |
| Память | `$readmemh`, `$readmemb`, `$writememh`, `$writememb` | Порядок адресов и расположение файла |
| Время | `$time`, `$stime`, `$realtime`, `$timeformat`, `$printtimescale` | Масштаб и точность |
| Форма массива | `$dimensions`, `$unpacked_dimensions`, `$left`, `$right`, `$low`, `$high`, `$increment`, `$size` | Номер размерности |
| Тип/размер | `$bits`, `$typename`, `$isunbounded` | Значение и тип — разные запросы |
| Биты | `$countbits`, `$countones`, `$onehot`, `$onehot0`, `$isunknown` | X/Z имеют специальное значение |
| Преобразования | `$signed`, `$unsigned`, `$cast`, `$itor`, `$rtoi` | Размер, знак и числовое значение |
| Представления real | `$realtobits`, `$bitstoreal`, `$shortrealtobits`, `$bitstoshortreal` | Битовая переинтерпретация |
| Математика | `$clog2`, `$ln`, `$log10`, `$exp`, `$sqrt`, `$pow`, `$floor`, `$ceil` | Не все вызовы — переносимый runtime RTL |
| Тригонометрия | `$sin`, `$cos`, `$tan`, `$asin`, `$acos`, `$atan`, `$atan2`, гиперболические варианты | Обычно модели real |
| Случайность | `$random`, `$urandom`, `$urandom_range`, `$dist_*` | Signed/unsigned и потоки seed |
| Аргументы запуска | `$test$plusargs`, `$value$plusargs` | Воспроизводимость прогона |
| Трасса | `$dumpfile`, `$dumpvars`, `$dumpon`, `$dumpoff`, `$dumpall`, `$dumplimit`, `$dumpflush` | Формат/поддержка инструмента |
| Выборка SVA | `$sampled`, `$past`, `$rose`, `$fell`, `$stable`, `$changed` | Работают с выбранными значениями |
| Контроль SVA | `$asserton`, `$assertoff`, `$assertkill`, `$assertcontrol`, семейства pass/fail/vacuous control | Проверки можно случайно отключить |
| Покрытие | `$get_coverage`, `$coverage_control`, `$coverage_get`, `$coverage_get_max`, `$coverage_merge`, `$coverage_save` | Поддержка и базы зависят от инструмента |
| Timing | `$setup`, `$hold`, `$setuphold`, `$recovery`, `$removal`, `$recrem`, `$width`, `$period` | Контекст specify |
| Аннотация | `$sdf_annotate` | Имена иерархии и библиотека должны совпасть |

В стандарте также есть средства очередей `$q_initialize/$q_add/$q_remove/
$q_full/$q_exam`, PLA-моделирования `$async$.../$sync$...` и глобальных
sampled-value запросов. Они специализированы и не нужны для базового RTL;
их точные сигнатуры нужно брать из соответствующего раздела LRM.

## Часто используемые методы

`string`: `len`, `getc`, `putc`, `tolower`, `toupper`, `compare`, `icompare`,
`substr`, `atoi`, `atohex`, `atooct`, `atobin`, `atoreal`, `itoa`, `hextoa`,
`octtoa`, `bintoa`, `realtoa`. Индексы строк обращаются к байтам, не к
произвольным Unicode-кодовым точкам; это важно для русского UTF-8.

Enum: `first`, `last`, `next`, `prev`, `num`, `name`.
Динамический массив: `size`, `delete`. Очередь дополнительно:
`insert`, `push_front/back`, `pop_front/back`.
Ассоциативный массив: `num`, `size`, `exists`, `first`, `last`, `next`, `prev`, `delete`.
Методы поиска, сортировки и свёрток разобраны в [главе 08](../02-data/08-arrays.md).

Random: `randomize`, `srandom`, `get_randstate`, `set_randstate`, `rand_mode`,
`constraint_mode`, callbacks `pre_randomize/post_randomize`.
Синхронизация: `mailbox`, `semaphore`, `process` — классы/средства `std`,
а не пользовательские аппаратные FIFO и арбитры.

## Форматные спецификаторы

`%b/%o/%d/%h` — основания целого, `%0d` убирает лишнюю ширину поля,
`%s` — строка, `%c` — символ, `%f/%e/%g` — real, `%t` — время,
`%p` — агрегатное представление, `%m` — область/иерархическое имя.
Не сравнивайте `%p`-строки разных симуляторов как нормативный формат протокола.
