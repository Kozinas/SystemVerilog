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
