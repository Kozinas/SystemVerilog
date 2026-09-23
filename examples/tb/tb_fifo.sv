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
