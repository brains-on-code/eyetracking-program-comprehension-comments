import java.util.HashSet;

public class Task4CM {
    public static int task4CM(int[] input) {
        HashSet<Integer> numSet = new HashSet<>();
        int maxLength = 0;

        for (int num : input) {
            numSet.add(num);
        }

        for (int num : input) {
            if (!numSet.contains(num - 1)) {
                int currentNum = num;
                int currentLength = 1;

                while (numSet.contains(currentNum + 1)) {
                    currentNum++;
                    currentLength++;
                }

                maxLength = Math.max(maxLength, currentLength);
            }
        }

        return maxLength;
    }

    public static void main(String[] args) {
        int[] input = {100, 4, 200, 1, 3, 2, 5};
        int result = task4CM(input);
        System.out.println(result);
    }
}