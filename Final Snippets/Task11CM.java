public class Task11CM {
    public static int task11CM(String str) {
        int count = 0;
        int n = str.length();

        for (int center = 0; center < 2 * n - 1; center++) {
            int left = center / 2;
            int right = left + center % 2;

            while (left >= 0 && right < n && str.charAt(left) == str.charAt(right)) {
                count++;
                left--;
                right++;
            }
        }

        return count;
    }

    public static void main(String[] args) {
        String input = "abba";
        int result = task11CM(input);
        System.out.println(result);
    }
}