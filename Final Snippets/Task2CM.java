import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;

public class Task2CM {
    public static List<Integer> task2CM(int[] input, int target) {
        HashSet<Integer> set = new HashSet<>();
        List<Integer> result = new ArrayList<>();

        for (int num : input) {
            if (set.contains(num)) {
                result.add(target - num);
                result.add(num);
                return result;
            }
            set.add(target - num);
        }

        return result;
    }

    public static void main(String[] args) {
        int[] input = {2, 4, 9, 5, 3, 1, 7};
        int target = 10;
        List<Integer> result = task2CM(input, target);
        System.out.println(result);
    }
}