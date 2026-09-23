module sv2023_demo;
  typedef union soft packed {
    logic [31:0] wide;
    logic [7:0] narrow;
  } overlay_t;
  overlay_t overlay;
  string description = """SystemVerilog 2023
multiline string""";
  logic persistent_flag;
  task automatic set_flag(ref static logic flag);
    flag = 1'b1;
  endtask
  initial begin
    overlay.wide = 32'h12345678;
    set_flag(persistent_flag);
    assert ($bits(overlay_t) == 32) else $fatal(1, "Union width");
    assert (overlay.narrow == 8'h78) else $fatal(1, "Union mapping");
    $display("%s", description);
    $finish;
  end
endmodule
