package zadanie8;

import java.util.Arrays;
import java.util.Comparator;

public class PermutationSort<T> {
    private final Comparator<T> comparator;

    public PermutationSort(Comparator<T> comparator) {
        this.comparator = comparator;
    }

    public void sort(T[] array) {
        while (!isSorted(array)) {
            nextPermutation(array);
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

    private boolean nextPermutation(T[] array) {
        int i = array.length - 2;
        while (i >= 0 && comparator.compare(array[i], array[i + 1]) >= 0) {
            i--;
        }
        if (i < 0) {
            reverse(array, 0, array.length - 1);
            return false;
        }
        int j = array.length - 1;
        while (comparator.compare(array[i], array[j]) >= 0) {
            j--;
        }
        swap(array, i, j);
        reverse(array, i + 1, array.length - 1);
        return true;
    }

    private void reverse(T[] array, int start, int end) {
        while (start < end) {
            swap(array, start++, end--);
        }
    }

    private void swap(T[] array, int i, int j) {
        T temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }

    public static void main(String[] args) {
        Comparator<Integer> comparator = Comparator.naturalOrder();
        Integer[] arr=new Integer[12];
        for (int i = 0; i < arr.length; i++) {
            arr[i] = (int) (Math.random() * 100);
        }

        new PermutationSort<>(comparator).sort(arr);
        System.out.println(Arrays.toString(arr));
    }
}