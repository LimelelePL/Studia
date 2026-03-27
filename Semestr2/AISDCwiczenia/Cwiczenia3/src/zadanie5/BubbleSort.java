package zadanie5;

import java.util.Comparator;

public class BubbleSort <T>{
    private final Comparator<T> comparator;
    public BubbleSort(Comparator<T> comparator) {
        this.comparator = comparator;
    }

    public void sort(T[] array) {
       for(int i=0; i<array.length; i++){
           for (int j = array.length - 1; j > i; j--) {
               if (comparator.compare(array[j], array[j - 1]) > 0) {
                   swap(array, j, j - 1);
               }
           }
              printArray(array);
       }
    }
    private void swap(T[] arr, int i, int j) {
        T temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
    private void printArray(T[] arr) {
        for (T value : arr) {
            System.out.print(value + " ");
        }
        System.out.println();
    }
    public static void main(String[] args) {
        Comparator<Integer> comparator = Comparator.naturalOrder();
        Integer[] arr = {76, 71, 5, 57, 12, 50, 20, 93, 20, 55, 62, 3};
        System.out.println("Bubble sort");
        BubbleSort<Integer> bubbleSort = new BubbleSort<>(comparator);
        bubbleSort.sort(arr);
    }
}
