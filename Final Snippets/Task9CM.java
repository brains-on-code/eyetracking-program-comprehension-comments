import java.util.ArrayList;
import java.util.List;

public class Task9CM {
    public static List<Integer> task9CM(int input) {
        boolean[] marks = new boolean[input + 1];
        List<Integer> numbers = new ArrayList<>();

        for (int num = 2; num <= input; num++) {
            if (!marks[num]) {
                numbers.add(num);
                for (int multiple = num * num; multiple <= input; multiple += num) {
                    marks[multiple] = true;
                }
            }
        }

        return numbers;
    }

    public static void main(String[] args) {
        int input = 18;
        List<Integer> result = task9CM(input);
        System.out.println(result);
    }
}
