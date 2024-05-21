public class Task11CP {
    public static int task11CP(String str) {
        int count = 0;          // Initialize the count of symmetrical substrings to zero
        int n = str.length();   // Get the length of the input string

        for (int center = 0; center < 2 * n - 1; center++) {    // Loop through each possible center (2n - 1)
            int left = center / 2;          // if the center is a character, left and right pointers are the same
            int right = left + center % 2;  // if the center is between two characters, left and right pointers are different

            while (left >= 0 && right < n && str.charAt(left) == str.charAt(right)) {   // Loop as long as the substring is symmetrical
                count++;    // Increment the count for each symmetrical substring found
                left--;     // Move the left pointer to the left to check the next character
                right++;    // Move the right pointer to the right to check the next character
            }
        }

        return count;       // Return the total count of symmetrical substrings
    }

    public static void main(String[] args) {
        String input = "abba";
        int result = task11CP(input);
        System.out.println(result);
    }
}