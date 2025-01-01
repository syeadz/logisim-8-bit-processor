// Example program to calculate the Fibonacci sequence
// up to the 13th number and display the result on the 7-segment display

int main()
{
    char a = 0; // fib 0
    char b = 1; // fib 1
    char c;

    // fib 2 to fib 13
    for (int i = 0; i < 12; i = i + 1) {
        c = a + b;
        a = b;
        b = c;
        SEG3 = a;
        SEG2 = b;
    }

    SEG0 = c;
}
