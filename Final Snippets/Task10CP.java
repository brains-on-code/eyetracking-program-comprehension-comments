public class Task10CP {
    public static int task10CP(int[] input, int target) {
        int left = 0;                                 // Initialize the left pointer
        int right = input.length - 1;                 // Initialize the right pointer

        while (left <= right) {
            int mid = left + (right - left) / 2;      // Calculate the mid index of the array (left + right) / 2

            if (input[mid] == target) {
                return mid;                           // If the target element is found, return the target index
            } else if (input[mid] < target) {
                left = mid + 1;                       // If the target is greater, the target is in the right half
            } else {
                right = mid - 1;                      // If the target is smaller, the target is in the left half
            }
        }

        return -1;                                    // If the target element is not found, return -1
    }

    public static void main(String[] args) {
        int[] input = {2, 5, 8, 12, 16, 23, 38, 45, 56, 72};
        int target = 45;
        int result = task10CP(input, target);
        System.out.println(result);
    }
}
