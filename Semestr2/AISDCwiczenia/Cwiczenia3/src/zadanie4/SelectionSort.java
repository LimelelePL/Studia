package zadanie4;

import java.util.Comparator;

public class SelectionSort <T>{
    private final Comparator<T> comparator;
    public SelectionSort(Comparator<T> comparator) {
        this.comparator = comparator;
    }
    public void sort(T[] array) {
        for(int i = 0; i<= array.length-1; i++){
            int maxIndex = i;
            for(int j=i; j<=array.length-1; j++){
                if(comparator.compare(array[j], array[maxIndex]) > 0){
                    maxIndex = j;
                }
            }
            swap(array, i, maxIndex);
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
        System.out.println("selection sort");
        SelectionSort<Integer> selectionSort = new SelectionSort<>(comparator);
        selectionSort.sort(arr);
    }
}
