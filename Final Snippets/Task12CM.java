import java.util.Arrays;

public class Task12CM {
    public static boolean task12CM(String input1, String input2) {
        if (input1.length() != input2.length()) {
            return false;
        }

        char[] charArray1 = input1.toCharArray();
        char[] charArray2 = input2.toCharArray();

        Arrays.sort(charArray1);
        Arrays.sort(charArray2);

        return Arrays.equals(charArray1, charArray2);
    }

    public static void main(String[] args) {
        String input1 = "listen";
        String input2 = "silent";
        boolean result = task12CM(input1, input2);
        System.out.println(result);
    }
}