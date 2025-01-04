module CONTROL_UNIT (
    input logic clk,
    input logic rst,
    input logic [5:0] opcode,
    input logic z_flag,
    input logic c_flag,
    output logic [3:0] alu_opcode,
    output logic mux_reg_mem_write,
    output logic mux_skip_alu_out,
    output logic pc_en,
    output logic reg_write_en,
    output logic mux_load_imm,
    output logic mem_write_en,
    output logic mux_pc_branch,
    output logic c_cond,
    output logic call,
    output logic ret
);

    logic call_, goto, ret_, reti, di, ei, sw, jpZ, jpNZ, jpC, jpNC, lwi, mov, xnor_, or_, and_, add, adc, sub, sbc, asr, rrc, ror, rol, lw;
    
    logic carry_reg;
    logic zero_reg;
    logic carry_reg_en;

    initial begin
        alu_opcode = 4'b0000;
        mux_reg_mem_write = 0;
        mux_skip_alu_out = 0;
        pc_en = 1;
        reg_write_en = 0;
        mux_load_imm = 0;
        mem_write_en = 0;
        mux_pc_branch = 0;
        c_cond = 0;
        call = 0;
        ret = 0;

        carry_reg = 0;
        zero_reg = 0;
    end

    always_comb begin
        pc_en = 1;

        c_cond = carry_reg;
        carry_reg_en = add || adc || rrc || ror || rol || sbc || sub || xnor_ || or_ || and_ || asr;

        casez (opcode)
            6'b0000??: begin // CALL
            call_ = 1;
            mux_reg_mem_write = 0;
            mux_skip_alu_out = 0;
            reg_write_en = 0;
            mux_load_imm = 0;
            mem_write_en = 0;
            mux_pc_branch = 1;
            call = 1;
            ret = 0;
            alu_opcode = 4'b0000;
            end
            6'b0001??: begin // GOTO
            goto = 1;
            mux_reg_mem_write = 0;
            mux_skip_alu_out = 0;
            reg_write_en = 0;
            mux_load_imm = 0;
            mem_write_en = 0;
            mux_pc_branch = 1;
            call = 0;
            ret = 0;
            alu_opcode = 4'b0000;
            end
            6'b001000: begin // RET
            ret_ = 1;
            mux_reg_mem_write = 0;
            mux_skip_alu_out = 0;
            reg_write_en = 0;
            mux_load_imm = 0;
            mem_write_en = 0;
            mux_pc_branch = 1;
            call = 0;
            ret = 1;
            alu_opcode = 4'b0000;
            end
            6'b001001: begin // RETI
            // unimplemented
            end
            6'b001010: begin // DI
            // unimplemented
            end
            6'b001011: begin // EI
            // unimplemented
            end
            6'b001100: begin // SW
            sw = 1;
            mux_reg_mem_write = 0;
            mux_skip_alu_out = 0;
            reg_write_en = 0;
            mux_load_imm = 0;
            mem_write_en = 1;
            mux_pc_branch = 0;
            call = 0;
            ret = 0;
            alu_opcode = 4'b0000;
            end
            6'b0100??: begin // JPZ
            jpZ = 1;
            mux_reg_mem_write = 0;
            mux_skip_alu_out = 0;
            reg_write_en = 0;
            mux_load_imm = 0;
            mem_write_en = 0;
            mux_pc_branch = zero_reg;
            call = 0;
            ret = 0;
            alu_opcode = 4'b0000;
            end
            6'b0101??: begin // JPNZ
            jpNZ = 1;
            mux_reg_mem_write = 0;
            mux_skip_alu_out = 0;
            reg_write_en = 0;
            mux_load_imm = 0;
            mem_write_en = 0;
            mux_pc_branch = ~zero_reg;
            call = 0;
            ret = 0;
            alu_opcode = 4'b0000;
            end
            6'b0110??: begin // JPC
            jpC = 1;
            mux_reg_mem_write = 0;
            mux_skip_alu_out = 0;
            reg_write_en = 0;
            mux_load_imm = 0;
            mem_write_en = 0;
            mux_pc_branch = carry_reg;
            call = 0;
            ret = 0;
            alu_opcode = 4'b0000;
            end
            6'b0111??: begin // JPNC
            jpNC = 1;
            mux_reg_mem_write = 0;
            mux_skip_alu_out = 0;
            reg_write_en = 0;
            mux_load_imm = 0;
            mem_write_en = 0;
            mux_pc_branch = ~carry_reg;
            call = 0;
            ret = 0;
            alu_opcode = 4'b0000;
            end
            6'b10????: begin // LWI
            lwi = 1;
            mux_reg_mem_write = 0;
            mux_skip_alu_out = 0;
            reg_write_en = 1;
            mux_load_imm = 1;
            mem_write_en = 0;
            mux_pc_branch = 0;
            call = 0;
            ret = 0;
            alu_opcode = 4'b0000;
            end
            6'b110000: begin // MOV
            mov = 1;
            mux_reg_mem_write = 0;
            mux_skip_alu_out = 1;
            reg_write_en = 1;
            mux_load_imm = 0;
            mem_write_en = 0;
            mux_pc_branch = 0;
            call = 0;
            ret = 0;
            alu_opcode = 4'b0000;
            end
            6'b110001: begin // XNOR
            xnor_ = 1;
            mux_reg_mem_write = 0;
            mux_skip_alu_out = 0;
            reg_write_en = 1;
            mux_load_imm = 0;
            mem_write_en = 0;
            mux_pc_branch = 0;
            call = 0;
            ret = 0;
            alu_opcode = 4'b0111;
            end
            6'b110010: begin // OR
            or_ = 1;
            mux_reg_mem_write = 0;
            mux_skip_alu_out = 0;
            reg_write_en = 1;
            mux_load_imm = 0;
            mem_write_en = 0;
            mux_pc_branch = 0;
            call = 0;
            ret = 0;
            alu_opcode = 4'b0101;
            end
            6'b110011: begin // AND
            and_ = 1;
            mux_reg_mem_write = 0;
            mux_skip_alu_out = 0;
            reg_write_en = 1;
            mux_load_imm = 0;
            mem_write_en = 0;
            mux_pc_branch = 0;
            call = 0;
            ret = 0;
            alu_opcode = 4'b0100;
            end
            6'b110100: begin // ADD
            add = 1;
            mux_reg_mem_write = 0;
            mux_skip_alu_out = 0;
            reg_write_en = 1;
            mux_load_imm = 0;
            mem_write_en = 0;
            mux_pc_branch = 0;
            call = 0;
            ret = 0;
            alu_opcode = 4'b0000;
            end
            6'b110101: begin // ADC
            adc = 1;
            mux_reg_mem_write = 0;
            mux_skip_alu_out = 0;
            reg_write_en = 1;
            mux_load_imm = 0;
            mem_write_en = 0;
            mux_pc_branch = 0;
            call = 0;
            ret = 0;
            alu_opcode = 4'b0010;
            end
            6'b110110: begin // SUB
            sub = 1;
            mux_reg_mem_write = 0;
            mux_skip_alu_out = 0;
            reg_write_en = 1;
            mux_load_imm = 0;
            mem_write_en = 0;
            mux_pc_branch = 0;
            call = 0;
            ret = 0;
            alu_opcode = 4'b0001;
            end
            6'b110111: begin // SBC
            sbc = 1;
            mux_reg_mem_write = 0;
            mux_skip_alu_out = 0;
            reg_write_en = 1;
            mux_load_imm = 0;
            mem_write_en = 0;
            mux_pc_branch = 0;
            call = 0;
            ret = 0;
            alu_opcode = 4'b0011;
            end
            6'b111000: begin // ASR
            asr = 1;
            mux_reg_mem_write = 0;
            mux_skip_alu_out = 0;
            reg_write_en = 1;
            mux_load_imm = 0;
            mem_write_en = 0;
            mux_pc_branch = 0;
            call = 0;
            ret = 0;
            alu_opcode = 4'b1000;
            end
            6'b111001: begin // RRC
            rrc = 1;
            mux_reg_mem_write = 0;
            mux_skip_alu_out = 0;
            reg_write_en = 1;
            mux_load_imm = 0;
            mem_write_en = 0;
            mux_pc_branch = 0;
            call = 0;
            ret = 0;
            alu_opcode = 4'b1101;
            end
            6'b111010: begin // ROR
            ror = 1;
            mux_reg_mem_write = 0;
            mux_skip_alu_out = 0;
            reg_write_en = 1;
            mux_load_imm = 0;
            mem_write_en = 0;
            mux_pc_branch = 0;
            call = 0;
            ret = 0;
            alu_opcode = 4'b1100;
            end
            6'b111011: begin // ROL
            rol = 1;
            mux_reg_mem_write = 0;
            mux_skip_alu_out = 0;
            reg_write_en = 1;
            mux_load_imm = 0;
            mem_write_en = 0;
            mux_pc_branch = 0;
            call = 0;
            ret = 0;
            alu_opcode = 4'b1011;
            end
            6'b1111??: begin // LW
            lw = 1;
            mux_reg_mem_write = 1;
            mux_skip_alu_out = 0;
            reg_write_en = 1;
            mux_load_imm = 0;
            mem_write_en = 0;
            mux_pc_branch = 0;
            call = 0;
            ret = 0;
            alu_opcode = 4'b0000;
            end
        endcase
    end

    always_ff @( posedge clk ) begin
        if (rst) begin
            carry_reg <= 0;
            zero_reg <= 0;
        end else begin
            if (carry_reg_en) begin
                carry_reg <= c_flag;
            end
            if (reg_write_en) begin
                zero_reg <= z_flag;
            end
        end
    end
endmodule