primitive udp_and(output y, input a, b);
  table
    0 ? : 0;
    ? 0 : 0;
    1 1 : 1;
  endtable
endprimitive

module primitive_demo(input wire a, b, output wire y);
  timeunit 1ns;
  timeprecision 1ps;
  udp_and u_gate(y, a, b);
  specify
    specparam T = 0.2;
    (a => y) = T;
    (b => y) = T;
  endspecify
endmodule
