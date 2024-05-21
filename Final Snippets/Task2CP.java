import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;

public class Task2CP {
    public static List<Integer> task2CP(int[] input, int target) {
        HashSet<Integer> set = new HashSet<>();      // Store complements encountered
        List<Integer> result = new ArrayList<>();    // Store the result pair

        for (int num : input) {                      // Iterate through the array
            if (set.contains(num)) {                 // If the current number is a complement of a previous number
                result.add(target - num);            // Add the first number of the result pair
                result.add(num);                     // Add the second number of the result pair
                return result;
            }
            set.add(target - num);                   // Add the complement of the current number to the set
        }

        return result;                               // Return an empty list if no result is found
    }

    public static void main(String[] args) {
        int[] input = {2, 4, 9, 5, 3, 1, 7};
        int target = 10;
        List<Integer> result = task2CP(input, target);
        System.out.println(result);
    }
}