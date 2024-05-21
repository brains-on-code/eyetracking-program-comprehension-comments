public static int task10CM(int[] input, int target) {
    int left = 0;
    int right = input.length - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (input[mid] == target) {
            return mid;
        } else if (input[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    return -1;
}

public static void main(String[] args) {
    int[] input = {2, 5, 8, 12, 16, 23, 38, 45, 56, 72};
    int target = 45;
    int result = task10CM(input, target);
    System.out.println(result);
}
