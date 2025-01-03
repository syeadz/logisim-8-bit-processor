module DECODER_tb;

    // Parameters
    parameter WIDTH_IN = 4;
    parameter WIDTH_OUT = 2 ** WIDTH_IN;

    // Inputs
    logic [WIDTH_IN - 1:0] in;

    // Outputs
    logic [WIDTH_OUT - 1:0] out;

    // Instantiate the Unit Under Test (UUT)
    DECODER #(
        .WIDTH_IN(WIDTH_IN),
        .WIDTH_OUT(WIDTH_OUT)
    ) uut (
        .in(in),
        .out(out)
    );

    // Test vectors
    initial begin
        $dumpfile("DECODER_tb.vcd");
        $dumpvars(0, DECODER_tb);
        
        // Test case 1
        in = 4'b0000;
        #10;
        assert(out == 16'b0000000000000001);

        // Test case 2
        in = 4'b0001;
        #10;
        assert(out == 16'b0000000000000010);

        // Test case 3
        in = 4'b0010;
        #10;
        assert(out == 16'b0000000000000100);

        // Test case 4
        in = 4'b0011;
        #10;
        assert(out == 16'b0000000000001000);

        // Test case 5
        in = 4'b0100;
        #10;
        assert(out == 16'b0000000000010000);

        // Test case 6
        in = 4'b0101;
        #10;
        assert(out == 16'b0000000000100000);

        // Test case 7
        in = 4'b0110;
        #10;
        assert(out == 16'b0000000001000000);

        // Test case 8
        in = 4'b0111;
        #10;
        assert(out == 16'b0000000010000000);

        // Test case 9
        in = 4'b1000;
        #10;
        assert(out == 16'b0000000100000000);

        // Test case 10
        in = 4'b1001;
        #10;
        assert(out == 16'b0000001000000000);

        // Test case 11
        in = 4'b1010;
        #10;
        assert(out == 16'b0000010000000000);

        // Test case 12
        in = 4'b1011;
        #10;
        assert(out == 16'b0000100000000000);

        // Test case 13
        in = 4'b1100;
        #10;
        assert(out == 16'b0001000000000000);

        // Test case 14
        in = 4'b1101;
        #10;
        assert(out == 16'b0010000000000000);

        // Test case 15
        in = 4'b1110;
        #10;
        assert(out == 16'b0100000000000000);

        // Test case 16
        in = 4'b1111;
        #10;
        assert(out == 16'b1000000000000000);

        $display("All test cases passed.");
        $finish;
    end

endmodule