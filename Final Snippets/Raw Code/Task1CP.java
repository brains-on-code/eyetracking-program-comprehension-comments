public static int task1CP(int[] input) {
    int left = 0;                      // Initialize left pointer for the binary search
    int right = input.length - 1;      // Initialize right pointer for the binary search
    while (left < right) {
        int mid = left + (right - left) / 2;    // Calculate the index of the middle element
        if (input[mid] < input[mid + 1]) {      // If the middle element is smaller than the element to its right,
            left = mid + 1;                     // Move left pointer to the greater element
        } else {
            right = mid;                        // Move right pointer to the left
        }
    }
    return left;    // Return the index of the element
}

public static void main(String[] args) {
    int[] input = {1, 2, 1, 3, 5, 6, 4};
    int result = task1CP(input);
    System.out.println(result);
}
