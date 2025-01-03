module RAM_tb;
    // Declare signals for RAM_tb
    logic clk;               // Clock signal
    logic [4:0] addr;        // Address for RAM
    logic [7:0] data_in;     // Data input for RAM
    logic we;                // Write enable for RAM
    logic [7:0] data_out;    // Data output from RAM
    
    // Instantiate RAM module
    RAM uut (
        .clk(clk),
        .addr(addr),
        .data_in(data_in),
        .we(we),
        .data_out(data_out)
    );
    
    // Clock generation (50% duty cycle)
    always begin
        #5 clk = ~clk;  // Toggle clock every 5 time units
    end

    // Initialize signals and run the test
    initial begin
        $dumpfile("RAM_tb.vcd");
        $dumpvars(0, RAM_tb);

        // Initialize signals
        clk = 0;         // Initial clock state (low)
        addr = 5'b0;     // Initial address
        data_in = 8'b0;  // Initial data input
        we = 1'b0;       // Initial write enable (disabled)
        
        #10;  // Wait for 10 time units
        $display("RAM initialized with 0 at address %d: %h", addr, data_out);

        // Write data to RAM
        addr = 5'b00001;
        data_in = 8'b10101010;
        we = 1'b1;      // Enable write
        #10;            // Wait for 10 time units
        $display("Data written to RAM at address %d: %h", addr, data_in);

        // Disable write
        addr = 5'b0;
        we = 1'b0;
        #10;  // Wait for 10 time units

        // Read data from RAM
        addr = 5'b00001;
        we = 1'b0;  // Disable write (read operation)
        $display("Data read from RAM at address %d: %h", addr, data_out);

        // Stop simulation after a certain period
        #20;  // Wait for 20 time units
        $finish;  // End the simulation
    end
endmodule
