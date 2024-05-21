public static int task4CP(int[] input) {
    HashSet<Integer> numSet = new HashSet<>();   // Set to store unique elements of the array
    int maxLength = 0;                           // Variable to store the length of the  longest consecutive sequence
    for (int num : input) {
        numSet.add(num);                         // Add all elements to the set to remove duplicates and order
    }
    for (int num : input) {
        if (!numSet.contains(num - 1)) {         // Check if the current element is the start of a sequence
            int currentNum = num;                // Initialize the current number
            int currentLength = 1;               // Initialize the current sequence length
            while (numSet.contains(currentNum + 1)) {        // Continue counting the consecutive sequence
                currentNum++;
                currentLength++;
            }
            maxLength = Math.max(maxLength, currentLength);  // Update the maximum length if necessary
        }
    }
    return maxLength;                            // Return the max length
}

public static void main(String[] args) {
    int[] input = {100, 4, 200, 1, 3, 2, 5};
    int result = task4CP(input);
    System.out.println(result);
}
