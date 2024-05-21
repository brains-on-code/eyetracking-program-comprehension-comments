public class Task7CM {
    public static long task7CM(long input1, long input2) {
        long result = 1;

        while (input2 > 0) {
            if (input2 % 2 == 1) {
                result *= input1;
            }
            input1 *= input1;
            input2 /= 2;
        }

        return result;
    }

    public static void main(String[] args) {
        long input1 = 2;
        long input2 = 10;
        long result = task7CM(input1, input2);
        System.out.println(result);
    }
}
