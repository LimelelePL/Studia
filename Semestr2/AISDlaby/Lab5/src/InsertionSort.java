import core.AbstractSwappingSortingAlgorithm;

import java.util.Comparator;
import java.util.List;

public class InsertionSort<T> extends AbstractSwappingSortingAlgorithm<T> {

    public InsertionSort(Comparator<? super T> comparator) {
        super(comparator);
    }

    @Override
    public List<T> sort(List<T> list) {
        int size = list.size();
        for (int i = size - 2; i >= 0; i--) {
            T element = list.get(i);
            int pos = binarySearch(list, element, i + 1, size - 1);

            if (pos > i ) {
                int j = i;
                while (j < pos-1) {
                    swap(list, j, j + 1);
                    j++;
                }
            }
        }
        return list;
    }

    private int binarySearch(List<T> list, T element, int left, int right) {
        while (left <= right) {
            int mid = (left + right) / 2;
            int cmp = compare(element, list.get(mid));

            if (cmp <= 0) {
                right = mid - 1;
            } else {
                left = mid + 1;
            }
        }
        return left;
    }
}


