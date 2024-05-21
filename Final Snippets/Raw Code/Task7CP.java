public static long task7CP(long input1, long input2) {
    long result = 1;                  // Initialize the result to 1
    while (input2 > 0) {              // Loop until input2 is 0
        if (input2 % 2 == 1) {        // If input2 is odd (last binary digit is 1)
            result *= input1;         // multiply the result by input1
        }
        input1 *= input1;             // Square input1 to increase the power of the result by 2
        input2 /= 2;                  // Divide input2 by 2 to remove the last binary digit
    }
    return result;                    // Return the final result
}

public static void main(String[] args) {
    long input1 = 2;
    long input2 = 10;
    long result = task7CP(input1, input2);
    System.out.println(result);
}
