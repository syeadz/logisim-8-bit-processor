module ALU_8_BIT(
    input logic [7:0] d0,
    input logic [7:0] d1,
    input logic [3:0] alu_op,
    input logic c_in,
    output logic [7:0] y,
    output logic c_out
);

    logic [7:0] add, sub, adc, sbc, and_, or_, not_, xnor_;
    logic [7:0] asr, lsl, lsr, rol, ror, rrc;
    logic add_carry, sub_carry, adc_carry, sbc_carry, rrc_carry;

    always_comb begin
        add = d0 + d1;
        add_carry = (d0 + d1) < d0 || (d0 + d1) < d1;

        sub = d0 - d1;
        sub_carry = d0 < d1;

        adc = d0 + d1 + c_in;
        adc_carry = (d0 + d1 + c_in) < d0 || (d0 + d1 + c_in) < d1;

        sbc = d0 - d1 - c_in;
        sbc_carry = d0 < (d1 + c_in);

        and_ = d0 & d1;
        or_ = d0 | d1;
        not_ = ~d0;
        xnor_ = ~(d0 ^ d1);

        asr = {d0[7], d0[7:1]}; // Arithmetic shift right
        lsl = d0 << 1;
        lsr = d0 >> 1;

        rol = d0 << 1 | d0 >> 7;
        ror = d0 >> 1 | d0 << 7;
        rrc = d0 >> 1 | c_in << 7;
        rrc_carry = d0[0];

        case (alu_op)
            4'b0000: c_out = add_carry;
            4'b0001: c_out = sub_carry;
            4'b0010: c_out = adc_carry;
            4'b0011: c_out = sbc_carry;
            4'b1101: c_out = rrc_carry;
            default: c_out = 1'b0;
        endcase

        case (alu_op)
            4'b0000: y = add;
            4'b0001: y = sub;
            4'b0010: y = adc;
            4'b0011: y = sbc;
            4'b0100: y = and_;
            4'b0101: y = or_;
            4'b0110: y = not_;
            4'b0111: y = xnor_;
            4'b1000: y = asr;
            4'b1001: y = lsl;
            4'b1010: y = lsr;
            4'b1011: y = rol;
            4'b1100: y = ror;
            4'b1101: y = rrc;
            default: y = 8'h00;
        endcase
    end
endmodule
