public class Task1CM {
    public static int task1CM(int[] input) {
        int left = 0;
        int right = input.length - 1;

        while (left < right) {
            int mid = left + (right - left) / 2;
            if (input[mid] < input[mid + 1]) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }

        return left;
    }

    public static void main(String[] args) {
        int[] input = {1, 2, 1, 3, 5, 6, 4};
        int result = task1CM(input);
        System.out.println(result);
    }
}