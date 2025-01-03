module ROM_tb;

    // Testbench variables
    logic [9:0] addr;        // 10-bit address for the ROM
    logic [13:0] data;       // 14-bit data output from the ROM

    // Instantiate the ROM module
    ROM uut (
        .addr(addr),
        .data(data)
    );

    // Memory array to store expected data values
    logic [13:0] mem_expected [0:1023];

    // Testbench procedure
    initial begin
        // Open a waveform dump file
        $dumpfile("ROM_tb.vcd");
        $dumpvars(0, ROM_tb);

        // Read expected data values from file
        $readmemh("fib_hex.txt", mem_expected);

        // Test cases
        for (int i = 0; i <= 36; i++) begin
            addr = i;
            #10;  // Wait for 10 time units
            if (data !== mem_expected[i]) begin
                $display("Mismatch at address %d: Expected %h, Got %h", i, mem_expected[i], data);
            end
        end

        // Finish simulation
        $finish;
    end
endmodule
