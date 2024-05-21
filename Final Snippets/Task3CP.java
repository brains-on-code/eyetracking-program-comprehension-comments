import java.util.HashMap;

public class Task3CP {
    public static int task3CP(int[] input) {
        int maxLength = 0;               // Variable to store the length of the longest subarray
        int sum = 0;                     // Variable to keep track of the cumulative sum of elements
        HashMap<Integer, Integer> sumMap = new HashMap<>();  // Key: cumulative sum, Value: index of first occurrence

        for (int i = 0; i < input.length; i++) {  // Iterate through the input array
            sum += input[i];                      // if the same cumulative sum is encountered again, it means that
                                                  // the elements between the two occurrences have a sum of 0.
            if (sumMap.containsKey(sum)) {        // There is a subarray with the desired sum.
                maxLength = Math.max(maxLength, i - sumMap.get(sum));  // Update the maximum length if necessary
            } else {
                sumMap.put(sum, i);               // Otherwise, add the cumulative sum and its index to the map
            }
        }

        return maxLength;   // Return the length of the longest subarray
    }

    public static void main(String[] args) {
        int[] input = {15, -2, 2, -8, 1, 7, 10, 23};
        int result = task3CP(input);
        System.out.println(result);
    }
}
