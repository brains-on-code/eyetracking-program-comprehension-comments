public class Task6CM {
    public static int task6CM(int[] input) {
        int n = input.length;
        int maxLength = 0;
        int[] dp = new int[n];

        for (int i = 0; i < n; i++) {
            dp[i] = 1;
            for (int j = 0; j < i; j++) {
                if (input[i] > input[j]) {
                    dp[i] = Math.max(dp[i], dp[j] + 1);
                }
            }
        }

        for (int length : dp) {
            maxLength = Math.max(maxLength, length);
        }

        return maxLength;
    }

    public static void main(String[] args) {
        int[] input = {10, 9, 2, 5, 3, 7, 101, 18};
        int result = task6CM(input);
        System.out.println(result);
    }
}