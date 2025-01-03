module DECODER #(
    parameter WIDTH_IN = 2,
    parameter WIDTH_OUT = 2 ** WIDTH_IN
)(
    input logic [WIDTH_IN - 1:0] in,
    output logic [WIDTH_OUT - 1:0] out
);
    
    always_comb begin
        out = '0;
        out[in] = 1'b1;
    end
endmodule