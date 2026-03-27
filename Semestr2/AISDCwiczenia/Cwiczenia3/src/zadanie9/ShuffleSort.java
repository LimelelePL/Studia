package zadanie9;

import java.util.Comparator;
import java.util.Random;
import java.util.Arrays;

public class ShuffleSort<T> {
    private final Comparator<T> comparator;
    private final Random random = new Random();

    public ShuffleSort(Comparator<T> comparator) {
        this.comparator = comparator;
    }

    public void sort(T[] array) {
        while (!isSorted(array)) {
            shuffle(array);
        }
    }

    private boolean isSorted(T[] array) {
        for (int i = 1; i < array.length; i++) {
            if (comparator.compare(array[i - 1], array[i]) > 0) {
                return false;
            }
        }
        return true;
    }

    private void shuffle(T[] array) {
        for (int i = array.length - 1; i > 0; i--) {
            int j = random.nextInt(i + 1);
            T temp = array[i];
            array[i] = array[j];
            array[j] = temp;
        }
    }

    public static void main(String[] args) {
        Comparator<Integer> comparator = Comparator.naturalOrder();
        Integer[] arr=new Integer[13];
        for (int i = 0; i < arr.length; i++) {
            arr[i] = (int) (Math.random() * 100);
        }
        long start = System.currentTimeMillis();
        new ShuffleSort<>(comparator).sort(arr);
        long end = System.currentTimeMillis();
        System.out.println(Arrays.toString(arr));
        System.out.println("Czas: " + (end - start) + " ms");
    }
}