module RAM_tb;
    // Declare signals for RAM_tb
    logic [4:0] addr;
    logic [7:0] data_in;
    logic we;
    logic [7:0] data_out;
    
    // Instantiate RAM module
    RAM uut (
        .addr(addr),
        .data_in(data_in),
        .we(we),
        .data_out(data_out)
    );
    
    // Initialize signals
    initial begin
        $dumpfile("RAM_tb.vcd");
        $dumpvars(0, RAM_tb);

        addr = 5'b0;
        data_in = 8'b0;
        we = 1'b0;
        #10;  // Wait for 10 time units
        $display("RAM initialized with 0 at address %d: %h", addr, data_out);

        // Write data to RAM
        addr = 5'b00001;
        data_in = 8'b10101010;
        we = 1'b1;
        #10;  // Wait for 10 time units
        $display("Data written to RAM at address %d: %h", addr, data_in);
        
        addr = 5'b0;
        we = 1'b0;
        #10;  // Wait for 10 time units

        // Read data from RAM
        addr = 5'b00001;
        we = 1'b0;
        #10;  // Wait for 10 time units
        $display("Data read from RAM at address %d: %h", addr, data_out);
    end
endmodule