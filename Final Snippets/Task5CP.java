public class Task5CP {
    public static int task5CP(String input1, String input2) {
        int m = input1.length();                    // Length of the first string
        int n = input2.length();                    // Length of the second string
        int[][] dp = new int[m + 1][n + 1];         // 2D array to keep track of the lengths of common subsequences

        for (int i = 1; i <= m; i++) {              // Loop through each character of the first string
            for (int j = 1; j <= n; j++) {          // Loop through each character of the second string
                if (input1.charAt(i - 1) == input2.charAt(j - 1)) {   // If the characters match
                    dp[i][j] = dp[i - 1][j - 1] + 1;                  // add 1 to the length of the common subsequence
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);  // Otherwise, take the maximum of the previous
                }                                                     // lengths for the smaller parts of the strings
            }
        }

        return dp[m][n];                           // Return the maximum length
    }

    public static void main(String[] args) {
        String input1 = "abcde";
        String input2 = "ace";
        int result = task5CP(input1, input2);
        System.out.println(result);
    }
}