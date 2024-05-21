import java.util.ArrayList;
import java.util.List;

public class Task9CP {
    public static List<Integer> task9CP(int input) {
        boolean[] marks = new boolean[input + 1];     // Array to store marks for each number that is not prime
        List<Integer> numbers = new ArrayList<>();    // List to store the numbers

        for (int num = 2; num <= input; num++) {
            if (!marks[num]) {                        // If the current number is not marked as true
                numbers.add(num);                     // Add the number to the list
                for (int multiple = num * num; multiple <= input; multiple += num) {
                    marks[multiple] = true;           // Mark all multiples of the number as true
                }
            }
        }

        return numbers;                               // Return the list of numbers
    }

    public static void main(String[] args) {
        int input = 18;
        List<Integer> result = task9CP(input);
        System.out.println(result);
    }
}
