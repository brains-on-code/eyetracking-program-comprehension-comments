import java.util.HashMap;

public class Task3CM {
    public static int task3CM(int[] input) {
        int maxLength = 0;
        int sum = 0;
        HashMap<Integer, Integer> sumMap = new HashMap<>();

        for (int i = 0; i < input.length; i++) {
            sum += input[i];

            if (sumMap.containsKey(sum)) {
                maxLength = Math.max(maxLength, i - sumMap.get(sum));
            } else {
                sumMap.put(sum, i);
            }
        }

        return maxLength;
    }

    public static void main(String[] args) {
        int[] input = {15, -2, 2, -8, 1, 7, 10, 23};
        int result = task3CM(input);
        System.out.println(result);
    }
}
