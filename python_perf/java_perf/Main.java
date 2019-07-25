public class Main {

    public static void main(String[] args) {
        logTime("heavyCalculation", () -> heavyCalculation());
    }

    interface Function {
        void exec();
    }

    private static void logTime(String name, Function someFunc) {
        long start = System.currentTimeMillis();
        someFunc.exec();
        long end = System.currentTimeMillis();
        System.out.println(String.format("%s took: %ss", name, (end - start) / 1000.));
    }

    private static void heavyCalculation() { // took 0.109s
        long a = 0;
        for (int i = 0; i < 10000000; i++) {
            a += Math.pow(2, 10);
        }
        System.out.println(String.format("a: %s", a));
    }
}
