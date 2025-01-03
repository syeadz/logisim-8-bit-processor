module REGISTER_FILE_tb;

    // Testbench signals
    logic clk;
    logic rst;
    logic [3:0] read_addr0;
    logic [3:0] read_addr1;
    logic [3:0] write_addr;
    logic [7:0] write_data;
    logic write_enable;
    logic [7:0] read_data0;
    logic [7:0] read_data1;

    // Instantiate the REGISTER_FILE module
    REGISTER_FILE uut (
        .clk(clk),
        .rst(rst),
        .read_addr0(read_addr0),
        .read_addr1(read_addr1),
        .write_addr(write_addr),
        .write_data(write_data),
        .write_enable(write_enable),
        .read_data0(read_data0),
        .read_data1(read_data1)
    );

    // Clock generation
    always begin
        #5 clk = ~clk;  // Toggle the clock every 5 time units
    end

    // Stimulus generation
    initial begin
        $dumpfile("REGISTER_FILE_tb.vcd");
        $dumpvars(0, REGISTER_FILE_tb);

        // Initialize signals
        clk = 0;
        rst = 0;
        write_enable = 0;
        write_addr = 4'b0000;
        write_data = 8'b00000000;
        read_addr0 = 4'b0000;
        read_addr1 = 4'b0001;

        // Apply reset
        rst = 1;
        #10;
        rst = 0;
        
        // Test 1: Write to register 0 and read back
        write_addr = 4'b0000;
        write_data = 8'b10101010;
        write_enable = 1;
        #10;  // Wait for a clock cycle
        
        write_enable = 0;  // Disable write
        read_addr0 = 4'b0000;  // Read from register 0
        #10;  // Wait for a clock cycle
        
        // Test 2: Write to register 1 and read from both registers
        write_addr = 4'b0001;
        write_data = 8'b11110000;
        write_enable = 1;
        #10;  // Wait for a clock cycle
        
        write_enable = 0;  // Disable write
        read_addr0 = 4'b0000;  // Read from register 0
        read_addr1 = 4'b0001;  // Read from register 1
        #10;  // Wait for a clock cycle
        
        // Test 3: Write to multiple registers and read from them
        write_addr = 4'b0010;
        write_data = 8'b11001100;
        write_enable = 1;
        #10;  // Wait for a clock cycle
        
        write_addr = 4'b0011;
        write_data = 8'b00110011;
        #10;  // Wait for a clock cycle
        
        write_enable = 0;  // Disable write
        read_addr0 = 4'b0010;  // Read from register 2
        read_addr1 = 4'b0011;  // Read from register 3
        #10;  // Wait for a clock cycle
        
        // Test 4: Reset and check all registers
        rst = 1;
        #10;  // Wait for reset to propagate
        rst = 0;

        read_addr0 = 4'b0000;  // Read from register 0
        read_addr1 = 4'b0001;  // Read from register 1
        
        #20;  // Wait for a clock cycle
        $finish;  // End the simulation
    end
endmodule
