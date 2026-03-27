package zadanie6;

import java.util.Comparator;

public class ShakerSort <T>{
    private final Comparator<T> comparator;
    public ShakerSort(Comparator<T> comparator) {
        this.comparator = comparator;
    }

    public void sort(T[] array) {
        int start=0;
        int end=array.length-1;

        while (start<end){
            for (int i = start; i < end; i++) {
                if (comparator.compare(array[i], array[i + 1]) > 0) {
                    swap(array, i, i + 1);
                }
            }
            end--;
            printArray(array);

            for (int i = end; i > start; i--) {
                if (comparator.compare(array[i], array[i - 1]) < 0) {
                    swap(array, i, i - 1);
                }
            }
            start++;
            printArray(array);
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
        System.out.println("Shaker sort");
        ShakerSort<Integer> shakerSort = new ShakerSort<>(comparator);
        shakerSort.printArray(arr);
        shakerSort.sort(arr);
    }
}
