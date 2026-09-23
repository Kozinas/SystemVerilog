# 22. Сквозной проект: синхронный FIFO

Практическая цель — соединить параметры, память, арифметику указателей,
тактовое состояние и проверку порядка данных в одном небольшом устройстве.
Полные исходники находятся в [examples](../../examples/README.md):
[sync_fifo.sv](../../examples/rtl/sync_fifo.sv) и
[tb_fifo.sv](../../examples/tb/tb_fifo.sv).

## Контракт до реализации

FIFO имеет один такт, активный низким уровнем асинхронный сброс, входные
`in_valid/in_ready/in_data` и выходные `out_valid/out_ready/out_data`.
Ширина W и глубина DEPTH положительны. Передача принимается на posedge,
если valid и ready одновременно равны 1 непосредственно перед фронтом.

Источник сохраняет `in_valid` и `in_data`, пока вход не принят. FIFO сохраняет
`out_valid` и `out_data` при остановке потребителя. В сбросе оба признака
готовности/действительности на границе подавлены. Содержимое памяти не очищается;
после сброса count=0 и прежние данные недействительны.

Вариант намеренно простой: комбинационное чтение первого элемента, без bypass
при пустоте. Когда FIFO полон до фронта, новая запись запрещена даже при
одновременном чтении. Это часть контракта, а не пропущенная оптимизация.
Для block RAM с синхронным чтением потребуется другая организация выхода.

## Состояние и инварианты

Храним `read_ptr`, `write_ptr` и `count`. Ширина указателя — max(1, clog2(DEPTH)),
ширина count — max(1, clog2(DEPTH+1)). Указатели явно оборачиваются при DEPTH-1.

| Условие до фронта | Запись | Чтение | Новое count |
| --- | --- | --- | --- |
| Только входной handshake | Да | Нет | count+1 |
| Только выходной handshake | Нет | Да | count-1 |
| Оба handshake | Да | Да | count |
| Ни одного | Нет | Нет | count |

Инварианты: 0 ≤ count ≤ DEPTH; указатели находятся в диапазоне;
выданная последовательность — префикс принятой последовательности;
выход не меняет элемент при `out_valid && !out_ready`.
Счётчик обновляется из одной таблицы действий, чтобы одновременные операции
не стали двумя конфликтующими присваиваниями.

## Полный RTL

Этот листинг совпадает с автономным исходником примера.

```systemverilog
`default_nettype none
module sync_fifo #(
  parameter int unsigned W = 8,
  parameter int unsigned DEPTH = 4,
  localparam int unsigned PW = (DEPTH > 1) ? $clog2(DEPTH) : 1,
  localparam int unsigned CW = (DEPTH > 1) ? $clog2(DEPTH + 1) : 1
) (
  input  wire clk, rst_n,
  input  wire in_valid,
  output wire in_ready,
  input  wire [W-1:0] in_data,
  output wire out_valid,
  input  wire out_ready,
  output wire [W-1:0] out_data
);
  timeunit 1ns;
  timeprecision 1ps;
  logic [W-1:0] memory [0:DEPTH-1];
  logic [PW-1:0] read_ptr, write_ptr;
  logic [CW-1:0] count;
  wire push = in_valid && in_ready;
  wire pop = out_valid && out_ready;

  assign in_ready = rst_n && (count < CW'(DEPTH));
  assign out_valid = rst_n && (count != 0);
  assign out_data = out_valid ? memory[read_ptr] : '0;

  function automatic logic [PW-1:0] advance(input logic [PW-1:0] ptr);
    if (ptr == PW'(DEPTH - 1)) return '0;
    return ptr + 1'b1;
  endfunction

  // Memory has no reset: only accepted writes change its contents.
  always_ff @(posedge clk)
    if (push) memory[write_ptr] <= in_data;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      read_ptr <= '0;
      write_ptr <= '0;
      count <= '0;
    end else begin
      if (push) write_ptr <= advance(write_ptr);
      if (pop) read_ptr <= advance(read_ptr);
      case ({push, pop})
        2'b10: count <= count + 1'b1;
        2'b01: count <= count - 1'b1;
        default: count <= count;
      endcase
    end
  end

  initial begin
    if (W < 1 || DEPTH < 1) $fatal(1, "W and DEPTH must be positive");
  end
endmodule
`default_nettype wire
```

## Как устроен тест

Самопроверяющийся тестбенч хранит очередь ожидаемых данных в простом массиве.
Он меняет стимулы на negedge, перед следующим posedge вычисляет ожидаемые
handshake и проверяет доступные выходы. После фронта даёт NBA завершиться
и проверяет новое состояние интерфейса. Так тест не соперничает с DUT
за изменение входов в Active одного фронта.

Есть направленные фазы: сброс, пустое чтение, заполнение до отказа, остановка
потребителя, полное опустошение, одновременные передачи и сброс непустой очереди.
Псевдослучайная фаза с фиксированным начальным состоянием генератора проверяет
сочетания valid/ready и оборачивание указателей. Последующее опустошение проверяет
оставшиеся элементы. Незавершённая передача источника удерживается до принятия.

Тест запускается для DEPTH=1, DEPTH=3 и DEPTH=8; неполная степень двойки
обнаруживает ошибки wrap, единичная глубина — ошибки нулевых диапазонов.
Тайм-аут завершает зависший прогон с ошибкой, а любое несовпадение вызывает `$fatal`.

## Что доказывает проверка

Компиляция проверяет синтаксис, имена, типы и часть правил драйверов.
Симуляция проверяет поведение только для выполненных трасс. Она не доказывает
timing, вывод RAM или все возможные входные последовательности.
Фактически выполненные команды и результаты указаны в
[VALIDATION.md](../../VALIDATION.md); отсутствие симулятора не должно превращаться
в выдуманное сообщение PASS.

## Полный самопроверяющийся тестбенч

Листинг совпадает с `examples/tb/tb_fifo.sv`. Каждый экземпляр `fifo_case`
независимо запускает направленные и псевдослучайные сценарии; верхний модуль
ожидает успех всех трёх. Счётчики accepted/delivered включают и транзакции,
отброшенные сбросом, поэтому их итоговое равенство не требуется. Проверяется
опустошение эталонной очереди после последней фазы.

```systemverilog
`default_nettype none
module fifo_case #(parameter int W = 8, DEPTH = 3) (output logic done = 0);
  timeunit 1ns;
  timeprecision 1ps;
  logic clk = 0;
  logic rst_n = 0, in_valid = 0, out_ready = 0;
  logic [W-1:0] in_data = '0;
  wire in_ready, out_valid;
  wire [W-1:0] out_data;
  sync_fifo #(.W(W), .DEPTH(DEPTH)) dut(.*);
  always #5ns clk = ~clk;

  // Independent sequence model: no DUT pointer/wrap arithmetic.
  logic [W-1:0] expected [0:8191];
  int head = 0, tail = 0;
  int accepted = 0, delivered = 0, simultaneous = 0, blocked = 0;
  bit holding = 0;
  logic [W-1:0] held_data;
  bit source_pending = 0;
  logic [W-1:0] source_data;
  bit last_push = 0;
  int unsigned rng = 32'hC0DE_1234 + DEPTH;

  function automatic int unsigned next_random();
    rng ^= rng << 13;
    rng ^= rng >> 17;
    rng ^= rng << 5;
    return rng;
  endfunction

  task automatic check_interface();
    if (in_ready !== (rst_n && (tail - head < DEPTH)))
      $fatal(1, "DEPTH=%0d in_ready mismatch", DEPTH);
    if (out_valid !== (rst_n && (tail != head)))
      $fatal(1, "DEPTH=%0d out_valid mismatch", DEPTH);
    if (out_valid && out_data !== expected[head])
      $fatal(1, "DEPTH=%0d expected=%h got=%h", DEPTH, expected[head], out_data);
  endtask

  task automatic cycle(input bit want_push, want_pop,
                       input logic [W-1:0] value);
    bit take_input, take_output;
    @(negedge clk);
    // Keep an unaccepted source transaction stable, regardless of new wishes.
    if (!source_pending && want_push) begin
      source_pending = 1;
      source_data = value;
    end
    in_valid = source_pending;
    in_data = source_data;
    out_ready = want_pop;
    #1ns;
    check_interface();
    take_input = in_valid && in_ready;
    take_output = out_valid && out_ready;
    if (holding && (!out_valid || out_data !== held_data))
      $fatal(1, "DEPTH=%0d output changed under backpressure", DEPTH);
    holding = out_valid && !out_ready;
    held_data = out_data;
    if (in_valid && !in_ready) blocked++;
    @(posedge clk);
    if (take_output) begin head++; delivered++; end
    if (take_input) begin
      if (tail >= 8192) $fatal(1, "Reference storage exhausted");
      expected[tail] = in_data;
      tail++;
      accepted++;
      source_pending = 0;
    end
    if (take_input && take_output) simultaneous++;
    last_push = take_input;
    #1ns;
    check_interface();
  endtask

  task automatic reset_fifo();
    @(negedge clk);
    rst_n = 0;
    in_valid = 0;
    out_ready = 0;
    source_pending = 0;
    holding = 0;
    head = 0;
    tail = 0;
    #1ns;
    check_interface();
    repeat (2) @(negedge clk);
    rst_n = 1;
  endtask

  initial begin
    int unsigned random_word;
    reset_fifo();
    repeat (3) cycle(0, 1, '0); // Empty reads must not become transfers.
    for (int i = 0; i < DEPTH; i++) cycle(1, 0, W'(i + 10));
    repeat (3) cycle(1, 0, W'(99)); // Full stall, preserve pending input.
    cycle(1, 1, W'(77)); // Full FIFO reads but rejects this input edge.
    if (last_push) $fatal(1, "Full FIFO unexpectedly accepted input");
    repeat (DEPTH + 3) cycle(0, 1, '0);
    repeat (20) cycle(1, 1, W'(next_random()));
    cycle(1, 0, W'(42));
    reset_fifo(); // Discard buffered and pending transactions by contract.
    for (int i = 0; i < 600; i++) begin
      random_word = next_random();
      cycle(random_word[0], random_word[1], W'(random_word >> 8));
    end
    repeat (DEPTH + 3) cycle(0, 1, '0);
    if (head != tail || source_pending) $fatal(1, "Not drained");
    if (blocked == 0 || accepted < 30 || delivered < 30)
      $fatal(1, "Required scenarios not exercised");
    if (DEPTH > 1 && simultaneous == 0) $fatal(1, "No simultaneous transfers");
    $display("PASS FIFO W=%0d DEPTH=%0d accepted=%0d delivered=%0d both=%0d blocked=%0d",
             W, DEPTH, accepted, delivered, simultaneous, blocked);
    done = 1;
  end
endmodule

module tb_fifo;
  timeunit 1ns;
  timeprecision 1ps;
  wire done1, done3, done8;
  fifo_case #(.W(1), .DEPTH(1)) u1(.done(done1));
  fifo_case #(.W(8), .DEPTH(3)) u3(.done(done3));
  fifo_case #(.W(13), .DEPTH(8)) u8(.done(done8));
  initial begin
    wait (done1 && done3 && done8);
    $display("PASS ALL FIFO CASES");
    $finish;
  end
  initial begin
    #100us;
    $fatal(1, "Global timeout");
  end
endmodule
`default_nettype wire
```

## Запуск и ожидаемый результат

Сохраните два листинга в `sync_fifo.sv` и `tb_fifo.sv`. При установленном
Icarus Verilog команды для этой пары файлов:

```text
iverilog -g2012 -s tb_fifo -o fifo.vvp sync_fifo.sv tb_fifo.sv
vvp fifo.vvp
```

Ожидаются три строки `PASS FIFO` для W/DEPTH = 1/1, 8/3, 13/8 и итоговая
`PASS ALL FIFO CASES`. Ошибка данных, интерфейса или зависание вызывает
`$fatal` и не должна считаться успешным тестом. Стенд не требует поддержки
классов, constraint solver или SVA; их самостоятельные примеры находятся
в проверочной части курса.

## Самостоятельное развитие

Следующая полезная модификация — разрешить одновременную запись при полном FIFO
и чтении. Изменятся зависимость in_ready, условия записи и тест на границе.
Затем можно сделать зарегистрированный выход для RAM. Каждая модификация сначала
требует обновить контракт и эталонную модель, затем RTL.

## Упражнение 22

При полном FIFO `in_valid=1`, `out_ready=1`. Какие операции примет текущая
реализация на ближайшем фронте? Сформулируйте новое условие in_ready для
варианта с замещением, не забыв про сброс.
