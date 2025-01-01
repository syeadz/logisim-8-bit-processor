// Example program that uses a for loop to count from 0 to 9.
// and write the value of i to the SEG0 register.

int main() {
    for (char i = 0; i < 10; i = i + 1) {
        SEG0 = i;
    }
}