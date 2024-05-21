public class Task5CM {
    public static int task5CM(String input1, String input2) {
        int m = input1.length();
        int n = input2.length();
        int[][] dp = new int[m + 1][n + 1];

        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (input1.charAt(i - 1) == input2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }

        return dp[m][n];
    }

    public static void main(String[] args) {
        String input1 = "abcde";
        String input2 = "ace";
        int result = task5CM(input1, input2);
        System.out.println(result);
    }
}