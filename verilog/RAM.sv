module RAM (
    input logic [4:0] addr,    // 5-bit address for 32 locations
    input logic [7:0] data_in, // 8-bit data input
    input logic we,            // Write enable
    output logic [7:0] data_out // 8-bit data output
);

    // Declare RAM as a 2D array of 8-bit logic
    logic [7:0] ram [0:31];  // 32 locations, each 8 bits wide

    // Initialize RAM to 0
    initial begin
        for (int i = 0; i < 32; i = i + 1) begin
            ram[i] = 8'b0;
        end
    end

    always_comb begin
        if (we) begin
            ram[addr] = data_in;
        end
        data_out = ram[addr];
    end
    
endmodule