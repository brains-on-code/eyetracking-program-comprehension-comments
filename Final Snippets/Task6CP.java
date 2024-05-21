public class Task6CP {
    public static int task6CP(int[] input) {
        int n = input.length;               // Length of the input array
        int maxLength = 0;                  // Variable to store the max length
        int[] dp = new int[n];              // Array to store lengths of subsequences that end at each index.

        for (int i = 0; i < n; i++) {       // Loop through each element of the input array
            dp[i] = 1;                      // Initialize the length of the subsequence to 1
            for (int j = 0; j < i; j++) {   // Loop through each element before the current element
                if (input[i] > input[j]) {  // If the current element can be included in the increasing subsequence
                    dp[i] = Math.max(dp[i], dp[j] + 1);  // Update the length of the subsequence if necessary
                }
            }
        }

        for (int length : dp) {
            maxLength = Math.max(maxLength, length);  // Find the maximum length from the array
        }

        return maxLength;                             // Return the maximum length
    }

    public static void main(String[] args) {
        int[] input = {10, 9, 2, 5, 3, 7, 101, 18};
        int result = task6CP(input);
        System.out.println(result);
    }
}