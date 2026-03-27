package zadanie6;

import java.util.Comparator;

public class UpdatedShakerSort <T>{
    private final Comparator<T> comparator;

    public UpdatedShakerSort(Comparator<T> comparator) {
        this.comparator = comparator;
    }

    public void sort(T[] array) {
        int start = 0;
        int end = array.length - 1;

        while (start < end) {
            boolean swapped = false;
            int lastSwap = start;

            for (int i = start; i < end; i++) {
                if (comparator.compare(array[i], array[i + 1]) > 0) {
                    swap(array, i, i + 1);
                    lastSwap = i;//susprawnienie zapamietanie ostatniego swapa
                    swapped = true;
                }
            }
            end = lastSwap;
            printArray(array);

            if (!swapped) break; // usprawnienie wykrycie braku zmian

            swapped = false;
            lastSwap = end;

            for (int i = end; i > start; i--) {
                if (comparator.compare(array[i], array[i - 1]) < 0) {
                    swap(array, i, i - 1);
                    lastSwap = i;
                    swapped = true;
                }
            }
            start = lastSwap;
            printArray(array);

            if (!swapped) break;
        }
    }



    private void printArray(T[] arr) {
        for (T value : arr) {
            System.out.print(value + " ");
        }
        System.out.println();
    }

    private void swap(T[] arr, int i, int j) {
        T temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    public static void main(String[] args) {
        Comparator<Integer> comparator = Comparator.naturalOrder();
        Integer[] arr = {76, 71, 5, 57, 12, 50, 20, 93, 20, 55, 62, 3};
        System.out.println("Updated Shaker sort");
        UpdatedShakerSort<Integer> updatedShakerSort = new UpdatedShakerSort<>(comparator);
        updatedShakerSort.sort(arr);
    }
}
