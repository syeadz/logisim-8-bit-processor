module RAM_ASYNC_READ_tb;
    // Declare signals for RAM_tb
    logic clk;               // Clock signal
    logic [4:0] addr;        // Address for RAM
    logic [7:0] data_in;     // Data input for RAM
    logic we;                // Write enable for RAM
    logic [7:0] data_out;    // Data output from RAM
    
    // Instantiate RAM module
    RAM_ASYNC_READ uut (
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
        $dumpfile("RAM_ASYNC_READ_tb.vcd");
        $dumpvars(0, RAM_ASYNC_READ_tb);

        // Initialize signals
        clk = 0;         // Initial clock state (low)
        addr = 5'b0;     // Initial address
        data_in = 8'b0;  // Initial data input
        we = 1'b0;       // Initial write enable (disabled)
        
        #10;  // Wait for 10 time units
        $display("RAM initialized with 0 at address %d: %h", addr, data_out);
        assert(data_out == 8'b0) else $fatal(1, "Initialization failed");

        // Write data to RAM at address 1
        addr = 5'b00001;
        data_in = 8'b10101010;
        we = 1'b1;      // Enable write
        #10;            // Wait for 10 time units
        $display("Data written to RAM at address %d: %h", addr, data_in);
        assert(data_out == 8'b10101010) else $fatal(1, "Write failed");

        // Disable write
        addr = 5'b0;
        we = 1'b0;
        #10;  // Wait for 10 time units

        // Read data from RAM at address 0
        addr = 5'b0;
        we = 1'b0;  // Disable write (read operation)
        #10
        $display("Data read from RAM at address %d: %h", addr, data_out);
        assert(data_out == 8'b0) else $fatal(1, "Read failed");

        // Read data from RAM at address 1
        addr = 5'b00001;
        #10;
        $display("Data read from RAM at address %d: %h", addr, data_out);
        assert(data_out == 8'b10101010) else $fatal(1, "Read failed");

        // Stop simulation after a certain period
        #20;  // Wait for 20 time units
        $finish;  // End the simulation
    end
endmodule
