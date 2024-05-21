import java.util.Arrays;

public class Task12CP {
    public static boolean task12CP(String input1, String input2) {
        if (input1.length() != input2.length()) {   // If the lengths are different, return false
            return false;
        }

        char[] charArray1 = input1.toCharArray();  // Convert the first string to a character array
        char[] charArray2 = input2.toCharArray();  // Convert the second string to a character array

        Arrays.sort(charArray1);  // Sort the character arrays
        Arrays.sort(charArray2);

        return Arrays.equals(charArray1, charArray2);  // Check if the sorted arrays are equal
    }

    public static void main(String[] args) {
        String input1 = "listen";
        String input2 = "silent";
        boolean result = task12CP(input1, input2);
        System.out.println(result);
    }
}