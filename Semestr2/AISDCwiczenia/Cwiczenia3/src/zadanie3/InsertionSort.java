package zadanie3;

import java.util.Comparator;

public class InsertionSort<T> {
    private final Comparator<T> comparator;
    public InsertionSort(Comparator<T> comparator) {
        this.comparator = comparator;
    }

    public void sort(T[] array) {
        for(int i= 1; i<=array.length-1; i++) {
            int j = i-1;
            T temp = array[i];
            while(j>=0 && comparator.compare(array[j], temp) < 0) {
                array[j + 1] = array[j];
                j--;
            }
            array[j + 1] = temp;
            printArray(array);
        }
    }

    public  void printArray(T[] arr) {
        for (T value : arr) {
            System.out.print(value + " ");
        }
        System.out.println();
    }

    public static void main(String[] args) {
        Comparator<Integer> comparator=Comparator.naturalOrder();

        Integer[] arr = {76, 71, 5, 57, 12, 50, 20, 93, 20, 55, 62, 3};
        InsertionSort<Integer> insertionSort = new InsertionSort<Integer>(comparator);
        insertionSort.sort(arr);


    }
}
