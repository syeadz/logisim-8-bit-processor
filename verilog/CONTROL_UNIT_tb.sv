module CONTROL_UNIT_tb;

    // Inputs
    logic clk;
    logic rst;
    logic [5:0] opcode;
    logic z_flag;
    logic c_flag;

    // Outputs
    logic [3:0] alu_opcode;
    logic mux_reg_mem_write;
    logic mux_skip_alu_out;
    logic pc_en;
    logic reg_write_en;
    logic mux_load_imm;
    logic mem_write_en;
    logic mux_pc_branch;
    logic c_cond;
    logic call;
    logic ret;

    // Instantiate the Unit Under Test (UUT)
    CONTROL_UNIT uut (
        .clk(clk),
        .rst(rst),
        .opcode(opcode),
        .z_flag(z_flag),
        .c_flag(c_flag),
        .alu_opcode(alu_opcode),
        .mux_reg_mem_write(mux_reg_mem_write),
        .mux_skip_alu_out(mux_skip_alu_out),
        .pc_en(pc_en),
        .reg_write_en(reg_write_en),
        .mux_load_imm(mux_load_imm),
        .mem_write_en(mem_write_en),
        .mux_pc_branch(mux_pc_branch),
        .c_cond(c_cond),
        .call(call),
        .ret(ret)
    );

    // Clock generation
    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end

    // Test stimulus
    initial begin
        $dumpfile("CONTROL_UNIT_tb.vcd");
        $dumpvars(0, CONTROL_UNIT_tb);

        // Initialize Inputs
        rst = 1;
        opcode = 6'b000000;
        z_flag = 0;
        c_flag = 0;

        // Wait for global reset
        #10;
        rst = 0;

        // Test CALL instruction
        opcode = 6'b000000;
        #10;
        assert(call == 1);
        assert(mux_pc_branch == 1);
        assert(alu_opcode == 4'b0000);

        // Test GOTO instruction
        opcode = 6'b000100;
        #10;
        assert(call == 0);
        assert(mux_pc_branch == 1);
        assert(alu_opcode == 4'b0000);

        // Test RET instruction
        opcode = 6'b001000;
        #10;
        assert(ret == 1);
        assert(mux_pc_branch == 1);
        assert(alu_opcode == 4'b0000);

        // Test SW instruction
        opcode = 6'b001100;
        #10;
        assert(mem_write_en == 1);
        assert(alu_opcode == 4'b0000);



        // Test JPZ instruction
        // Set zero_reg to 1
        opcode = 6'b110100;
        z_flag = 1;
        #10;

        opcode = 6'b010000;
        #10;
        assert(mux_pc_branch == 1);
        assert(alu_opcode == 4'b0000);

        // Test JPNZ instruction
        // Set zero_reg to 0
        opcode = 6'b110100;
        z_flag = 0;
        #10;

        opcode = 6'b010100;
        #10;
        assert(mux_pc_branch == 1);
        assert(alu_opcode == 4'b0000);

        // Test JPC instruction
        // Set c_flag to 1
        opcode = 6'b110100;
        c_flag = 1;
        #10;

        opcode = 6'b011000;
        #10;
        assert(mux_pc_branch == 1);
        assert(alu_opcode == 4'b0000);

        // Test JPNC instruction
        // Set c_flag to 0
        opcode = 6'b110100;
        c_flag = 0;
        #10;

        opcode = 6'b011100;
        #10;
        assert(mux_pc_branch == 1);
        assert(alu_opcode == 4'b0000);

        // Test LWI instruction
        opcode = 6'b100000;
        #10;
        assert(reg_write_en == 1);
        assert(mux_load_imm == 1);
        assert(alu_opcode == 4'b0000);

        // Test MOV instruction
        opcode = 6'b110000;
        #10;
        assert(reg_write_en == 1);
        assert(mux_skip_alu_out == 1);
        assert(alu_opcode == 4'b0000);

        // Test XNOR instruction
        opcode = 6'b110001;
        #10;
        assert(reg_write_en == 1);
        assert(alu_opcode == 4'b0111);

        // Test OR instruction
        opcode = 6'b110010;
        #10;
        assert(reg_write_en == 1);
        assert(alu_opcode == 4'b0101);

        // Test AND instruction
        opcode = 6'b110011;
        #10;
        assert(reg_write_en == 1);
        assert(alu_opcode == 4'b0100);

        // Test ADD instruction
        opcode = 6'b110100;
        #10;
        assert(reg_write_en == 1);
        assert(alu_opcode == 4'b0000);

        // Test ADC instruction
        opcode = 6'b110101;
        #10;
        assert(reg_write_en == 1);
        assert(alu_opcode == 4'b0010);

        // Test SUB instruction
        opcode = 6'b110110;
        #10;
        assert(reg_write_en == 1);
        assert(alu_opcode == 4'b0001);
        // Test SBC instruction
        opcode = 6'b110111;
        #10;
        assert(reg_write_en == 1);
        assert(alu_opcode == 4'b0011);

        // Test ASR instruction
        opcode = 6'b111000;
        #10;
        assert(reg_write_en == 1);
        assert(alu_opcode == 4'b1000);

        // Test RRC instruction
        opcode = 6'b111001;
        #10;
        assert(reg_write_en == 1);
        assert(alu_opcode == 4'b1101);

        // Test ROR instruction
        opcode = 6'b111010;
        #10;
        assert(reg_write_en == 1);
        assert(alu_opcode == 4'b1100);

        // Test ROL instruction
        opcode = 6'b111011;
        #10;
        assert(reg_write_en == 1);
        assert(alu_opcode == 4'b1011);

        // Test LW instruction
        opcode = 6'b111100;
        #10;
        assert(mux_reg_mem_write == 1);
        assert(reg_write_en == 1);
        assert(alu_opcode == 4'b0000);

        $finish;
    end

endmodule