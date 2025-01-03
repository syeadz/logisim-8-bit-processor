module MUX #(
    parameter WIDTH = 8,
    parameter N = 2
)(
    input logic [WIDTH - 1:0] in [0:N-1],
    input logic [N - 1:0] sel,
    output logic [WIDTH - 1:0] out
);

    always_comb begin
        out = in[sel];
    end
endmodule