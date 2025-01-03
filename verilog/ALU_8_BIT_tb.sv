module ALU_8_BIT_tb;

    logic [7:0] d0;
    logic [7:0] d1;
    logic [3:0] alu_op;
    logic c_in;
    logic [7:0] y;
    logic c_out;

    ALU_8_BIT uut (
        .d0(d0),
        .d1(d1),
        .alu_op(alu_op),
        .c_in(c_in),
        .y(y),
        .c_out(c_out)
    );

    initial begin
        $dumpfile("ALU_8_BIT_tb.vcd");
        $dumpvars(0, ALU_8_BIT_tb);

        // Test case 1: Addition
        d0 = 8'h0A;
        d1 = 8'h05;
        alu_op = 4'b0000;
        c_in = 1'b0;
        #10;
        $display("Addition: y = %h, c_out = %b", y, c_out);
        assert(y == 8'h0F && c_out == 1'b0) else $fatal(1, "Test case 1 failed");

        // Test case 2: Subtraction
        d0 = 8'h0A;
        d1 = 8'h05;
        alu_op = 4'b0001;
        c_in = 1'b0;
        #10;
        $display("Subtraction: y = %h, c_out = %b", y, c_out);
        assert(y == 8'h05 && c_out == 1'b0) else $fatal(1, "Test case 2 failed");

        // Test case 3: AND
        d0 = 8'h0A;
        d1 = 8'h05;
        alu_op = 4'b0100;
        c_in = 1'b0;
        #10;
        $display("AND: y = %h", y);
        assert(y == 8'h00) else $fatal(1, "Test case 3 failed");

        // Test case 4: OR
        d0 = 8'h0A;
        d1 = 8'h05;
        alu_op = 4'b0101;
        c_in = 1'b0;
        #10;
        $display("OR: y = %h", y);
        assert(y == 8'h0F) else $fatal(1, "Test case 4 failed");

        // Test case 5: NOT
        d0 = 8'h0A;
        d1 = 8'h00;
        alu_op = 4'b0110;
        c_in = 1'b0;
        #10;
        $display("NOT: y = %h", y);
        assert(y == ~8'h0A) else $fatal(1, "Test case 5 failed");

        // Test case 6: XNOR
        d0 = 8'h0A;
        d1 = 8'h05;
        alu_op = 4'b0111;
        c_in = 1'b0;
        #10;
        $display("XNOR: y = %h", y);
        assert(y == ~(8'h0A ^ 8'h05)) else $fatal(1, "Test case 6 failed");

        // Test case 7: Arithmetic Shift Right
        d0 = 8'h0A;
        d1 = 8'h00;
        alu_op = 4'b1000;
        c_in = 1'b0;
        #10;
        $display("ASR: y = %h", y);
        assert(y == 8'h05) else $fatal(1, "Test case 7 failed");

        // Test case 8: Logical Shift Left
        d0 = 8'h0A;
        d1 = 8'h00;
        alu_op = 4'b1001;
        c_in = 1'b0;
        #10;
        $display("LSL: y = %h", y);
        assert(y == 8'h14) else $fatal(1, "Test case 8 failed");

        // Test case 9: Logical Shift Right
        d0 = 8'h0A;
        d1 = 8'h00;
        alu_op = 4'b1010;
        c_in = 1'b0;
        #10;
        $display("LSR: y = %h", y);
        assert(y == 8'h05) else $fatal(1, "Test case 9 failed");

        // Test case 10: Rotate Left
        d0 = 8'h0A;
        d1 = 8'h00;
        alu_op = 4'b1011;
        c_in = 1'b0;
        #10;
        $display("ROL: y = %h", y);
        assert(y == 8'h14) else $fatal(1, "Test case 10 failed");

        // Test case 11: Rotate Right
        d0 = 8'h0A;
        d1 = 8'h00;
        alu_op = 4'b1100;
        c_in = 1'b0;
        #10;
        $display("ROR: y = %h", y);
        assert(y == 8'h05) else $fatal(1, "Test case 11 failed");

        // Test case 12: Rotate Right through Carry
        d0 = 8'h0A;
        d1 = 8'h00;
        alu_op = 4'b1101;
        c_in = 1'b1;
        #10;
        $display("RRC: y = %h, c_out = %b", y, c_out);
        assert(y == 8'h85 && c_out == 1'b0) else $fatal(1, "Test case 12 failed");

        // Test case 13: Add with carry-out
        d0 = 8'hFF;
        d1 = 8'h01;
        alu_op = 4'b0000;
        c_in = 1'b0;
        #10;
        $display("Addition with carry-out: y = %h, c_out = %b", y, c_out);
        assert(y == 8'h00 && c_out == 1'b1) else $fatal(1, "Test case 13 failed");

        // Test case 14: Subtract with carry-out
        d0 = 8'h00;
        d1 = 8'h01;
        alu_op = 4'b0001;
        c_in = 1'b0;
        #10;
        $display("Subtraction with carry-out: y = %h, c_out = %b", y, c_out);
        assert(y == 8'hFF && c_out == 1'b1) else $fatal(1, "Test case 14 failed");

        // Test case 15: Adc with carry-in
        d0 = 8'hFF;
        d1 = 8'h01;
        alu_op = 4'b0010;
        c_in = 1'b1;
        #10;
        $display("Adc with carry-in: y = %h, c_out = %b", y, c_out);
        assert(y == 8'h01 && c_out == 1'b1) else $fatal(1, "Test case 15 failed");

        // Test case 16: Sbc with carry-in
        d0 = 8'h00;
        d1 = 8'h01;
        alu_op = 4'b0011;
        c_in = 1'b1;
        #10;
        $display("Sbc with carry-in: y = %h, c_out = %b", y, c_out);
        assert(y == 8'hFE && c_out == 1'b1) else $fatal(1, "Test case 16 failed");

        // Test case 17: Rotate Right through Carry with carry-out
        d0 = 8'hFF;
        d1 = 8'h00;
        alu_op = 4'b1101;
        c_in = 1'b1;
        #10;
        $display("RRC with carry-out: y = %h, c_out = %b", y, c_out);
        assert(y == 8'hFF && c_out == 1'b1) else $fatal(1, "Test case 17 failed");

        // Stop simulation
        #20;
        $finish;
    end

endmodule
