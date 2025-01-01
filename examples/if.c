// Example program that uses if statements to compare two variables.
// and writes values to the SEG registers based on the comparison.

int main() {
    char a = 2;
    char b = 1;

    // False
    if (a < b) {
        SEG0 = a;
    }

    // True
    if (a > b) {
        SEG1 = b;
    }

    // True
    if (b < a) {
        SEG2 = a;
    }

    // False
    if (b > a) {
        SEG3 = b;
    }
}