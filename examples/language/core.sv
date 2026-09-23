package example_pkg;
  timeunit 1ns;
  timeprecision 1ps;
  typedef enum logic [1:0] {IDLE=0, READ=1, WRITE=2} opcode_t;
  typedef struct packed { opcode_t op; logic [7:0] data; } command_t;
  function automatic logic [8:0] add8(input logic [7:0] a, b);
    return {1'b0, a} + {1'b0, b};
  endfunction
endpackage

module core_demo;
  timeunit 1ns;
  timeprecision 1ps;
  import example_pkg::*;
  logic [7:0] a = 255, b = 1;
  logic [8:0] sum;
  logic signed [7:0] signed_value = -128;
  opcode_t op = IDLE;
  command_t command;
  int values[$];
  int selected[$];
  assign sum = add8(a, b);
  initial begin
    #1ns;
    assert (sum == 256) else $fatal(1, "Lost carry");
    assert ((signed_value >>> 1) == -64) else $fatal(1, "Signed shift");
    assert (!$cast(op, 2'b11)) else $fatal(1, "Invalid enum accepted");
    command = '{op: READ, data: 8'hA5};
    assert ($bits(command_t) == 10) else $fatal(1, "Wrong struct width");
    values = {1, 4, 7, 10};
    selected = values.find() with (item > 5);
    assert (selected.size() == 2) else $fatal(1, "Array filter");
    $display("PASS CORE");
    $finish;
  end
endmodule
