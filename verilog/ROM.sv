module ROM (
    input  logic [9:0] addr,    // 10-bit address for 1k locations
    output logic [13:0] data    // 14-bit data output
);

    // Declare ROM as a 2D array of 14-bit logic
    logic [13:0] rom [0:1023];  // 1k locations, each 14 bits wide

    // Initialize ROM from a file
    initial begin
        // Read hex values for fib program from file
        $readmemh("fib_hex.txt", rom);
    end

    always_comb begin
        data = rom[addr];
    end
endmodule
