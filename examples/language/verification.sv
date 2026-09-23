interface sample_if(input logic clk);
  timeunit 1ns;
  timeprecision 1ps;
  logic valid, ready;
  logic [7:0] data;
  clocking cb @(posedge clk);
    default input #1step output #0;
    input ready;
    output valid, data;
  endclocking
  modport source(output valid, data, input ready);
endinterface

class transaction;
  rand bit [7:0] address;
  rand int unsigned length;
  constraint legal {
    address inside {[0:127]};
    length inside {[1:8]};
    int'(address) + length <= 128;
  }
  function transaction clone();
    transaction result = new;
    result.address = address;
    result.length = length;
    return result;
  endfunction
endclass

class coverage_collector;
  covergroup cg with function sample(bit push, bit pop);
    option.per_instance = 1;
    put: coverpoint push;
    get: coverpoint pop;
    both: cross put, get;
  endgroup
  function new(); cg = new; endfunction
endclass

module verification_demo;
  timeunit 1ns;
  timeprecision 1ps;
  logic clk = 0, rst_n = 0;
  sample_if bus(clk);
  transaction item;
  coverage_collector coverage;
  mailbox #(transaction) channel = new(2);
  always #5ns clk = ~clk;
  assert property (@(posedge clk) disable iff (!rst_n)
    bus.valid && !bus.ready |=> bus.valid && $stable(bus.data));
  initial begin
    item = new;
    coverage = new;
    bus.valid = 0;
    bus.ready = 1;
    bus.data = 0;
    if (!item.randomize()) $fatal(1, "Constraints failed");
    channel.put(item.clone());
    coverage.cg.sample(1, 0);
    @(negedge clk);
    rst_n = 1;
    repeat (3) @(negedge clk);
    $finish;
  end
endmodule
