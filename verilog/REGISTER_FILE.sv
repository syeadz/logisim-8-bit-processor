module REGISTER_FILE (
    input logic clk,           // Clock signal
    input logic rst,          // Reset signal, synchronous active high
    input logic [3:0] read_addr0,    // 4-bit address for 16 locations
    input logic [3:0] read_addr1,    // 4-bit address for 16 locations
    input logic [3:0] write_addr,   // 4-bit address for 16 locations
    input logic [7:0] write_data, // 8-bit data input
    input logic write_enable,            // Write enable
    output logic [7:0] read_data0, // 8-bit data output
    output logic [7:0] read_data1 // 8-bit data output
);

    logic [7:0] registers [0:15];  // 16 locations, each 8 bits wide

    // Initialize registers to 0
    initial begin
        for (int i = 0; i < 16; i = i + 1) begin
            registers[i] = 8'b0;
        end
    end

    // Synchronous Write on clock edge
    always_ff @(posedge clk) begin
        if (rst) begin
            for (int i = 0; i < 16; i = i + 1) begin
                registers[i] = 8'b0;
            end
        end
        else if (write_enable) begin
            registers[write_addr] <= write_data;  // Write to registers on positive clock edge when 'write_enable' is high
        end
    end

    // Asynchronous Read
    always_comb begin
        read_data0 = registers[read_addr0];  // Output the value at the address immediately when read_addr0 changes
        read_data1 = registers[read_addr1];  // Output the value at the address immediately when read_addr1 changes
    end
endmodule