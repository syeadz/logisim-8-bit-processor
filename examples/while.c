// Example program that uses a while loop to count from 0 to 9.
// and write the value of a to the SEG0 register.

int main() {
    char a = 0;
    while (a < 10) {
        SEG0 = a;
        a = a + 1;
    }
}