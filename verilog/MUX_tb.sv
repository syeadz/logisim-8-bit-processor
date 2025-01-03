module MUX_tb;

    // Parameters
    parameter WIDTH = 8;
    parameter N = 2;

    // Inputs
    logic [WIDTH - 1:0] in [0:N-1];
    logic [N - 1:0] sel;

    // Outputs
    logic [WIDTH - 1:0] out;

    // Instantiate the Unit Under Test (UUT)
    MUX #(
        .WIDTH(WIDTH),
        .N(N)
    ) uut (
        .in(in),
        .sel(sel),
        .out(out)
    );

    initial begin
        // Initialize Inputs
        in[0] = 8'hAA;
        in[1] = 8'h55;
        sel = 0;

        // Wait for global reset
        #10;
        
        // Test case 1: Select input 0
        sel = 0;
        #10;
        $display("Test case 1: sel = %0d, out = %h (expected: %h)", sel, out, in[0]);
        assert(out == in[0])

        // Test case 2: Select input 1
        sel = 1;
        #10;
        $display("Test case 2: sel = %0d, out = %h (expected: %h)", sel, out, in[1]);
        assert(out == in[1])

        // Test case 3: Change inputs and select input 0
        in[0] = 8'hFF;
        in[1] = 8'h00;
        sel = 0;
        #10;
        $display("Test case 3: sel = %0d, out = %h (expected: %h)", sel, out, in[0]);
        assert(out == in[0])

        // Test case 4: Change inputs and select input 1
        sel = 1;
        #10;
        $display("Test case 4: sel = %0d, out = %h (expected: %h)", sel, out, in[1]);
        assert(out == in[1])

        $display("All test cases passed");
        $finish;
    end

endmodule