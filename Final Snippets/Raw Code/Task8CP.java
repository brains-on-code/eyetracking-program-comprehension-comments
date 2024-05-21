public static int task8CP(int input) {
    if (input <= 1) {
        return input;               // Return n if n is less than or equal to 1
    }
    int prev = 0;                   // Initialize the first number in the sequence
    int current = 1;                // Initialize the second number in the sequence
    for (int i = 2; i <= input; i++) {      // Iterate to find the nth number in the sequence
        int next = prev + current;          // Calculate the next number in the sequence
        prev = current;                     // Update the first number with the second number
        current = next;                     // Update the second number with the next number
    }
    return current;                 // Return the nth number in the sequence
}

public static void main(String[] args) {
    int input = 7;
    int result = task8CP(input);
    System.out.println(result);
}
