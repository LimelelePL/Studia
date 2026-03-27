
import core.AbstractSwappingSortingAlgorithm;
import pivot.PivotStrategy;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class QuickSort <T> extends AbstractSwappingSortingAlgorithm<T>  {
    private final PivotStrategy<T> selectPivot;

    public QuickSort(Comparator<? super T> comparator, PivotStrategy<T> selectPivot) {
        super(comparator);
        this.selectPivot = selectPivot;
    }

    @Override
    public List<T> sort(List<T> list) {
        if (list.isEmpty() || list.size() < 2) {
            return list;
        }

        ArrayList<T> temp = new ArrayList<>(list);
        temp.addAll(list);

        quickSort(temp, 0, list.size() - 1);

        list.clear();
        list.addAll(temp);

        return list;
    }

    private void quickSort(List<T> list, int lowIndex, int highIndex) {
        if (lowIndex >= highIndex) {
            return;
        }

        T pivot = selectPivot.selectPivot(list, lowIndex, highIndex);
        int pivotIndex = list.indexOf(pivot);
        swap(list, pivotIndex, highIndex);

        int leftPointer = lowIndex;
        int rightPointer = highIndex - 1;

        while (leftPointer <= rightPointer) {
            while (leftPointer <= rightPointer && compare(list.get(leftPointer), list.get(highIndex)) < 0) {
                leftPointer++;
            }

            while (rightPointer >= leftPointer && compare(list.get(rightPointer), list.get(highIndex)) > 0) {
                rightPointer--;
            }

            if (leftPointer <= rightPointer) {
                swap(list, leftPointer, rightPointer);
                leftPointer++;
                rightPointer--;
            }
        }

        swap(list, leftPointer, highIndex);
        quickSort(list, lowIndex, leftPointer - 1);
        quickSort(list, leftPointer + 1, highIndex);
    }
}
