public static int task8CM(int input) {
    if (input <= 1) {
        return input;
    }
    int prev = 0;
    int current = 1;
    for (int i = 2; i <= input; i++) {
        int next = prev + current;
        prev = current;
        current = next;
    }
    return current;
}

public static void main(String[] args) {
    int input = 7;
    int result = task8CM(input);
    System.out.println(result);
}
