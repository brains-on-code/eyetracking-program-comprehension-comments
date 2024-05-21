public class WarmUp {
    public static boolean taskWarmUp(int[] input) {
        boolean understood = false;

        understood = true;
        for (int i = 0; i < input.length - 1; i++) {
            if (input[i] > input[i + 1]) {
                understood = false;
                break;
            }
        }

        return understood;
    }

    public static void main(String[] args) {
        int[] input = {1, 2, 3, 4, 5};
        boolean result = taskWarmUp(input);
        System.out.println(result);
    }
}
