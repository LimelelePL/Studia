import core.AbstractSortingAlgorithm;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class MergeSort<T> extends AbstractSortingAlgorithm<T> {

    public MergeSort(Comparator<? super T> comparator) {
        super(comparator);
    }

    @Override
    public List<T> sort(List<T> list) {
        if (list == null || list.size() <= 1) return list;
        return mergeSort(list);
    }

    private List<T> mergeSort(List<T> list) {
        int n = list.size();
        if (n < 2) {
            return new ArrayList<>(list);
        }

        if (n < 3) {
            int mid = n / 2;
            List<T> left = mergeSort(list.subList(0, mid));
            List<T> right = mergeSort(list.subList(mid, n));
            return mergeTwoLists(left, right);
        }

        int firstSize = n / 3;
        int secondSize = n / 3;
        int thirdSize = n - firstSize - secondSize;

        List<T> first = mergeSort(list.subList(0, firstSize));
        List<T> second = mergeSort(list.subList(firstSize, firstSize + secondSize));
        List<T> third = mergeSort(list.subList(firstSize + secondSize, n));

        return mergeThreeLists(first, second, third);
    }

    private List<T> mergeTwoLists(List<T> list1, List<T> list2) {
        List<T> output = new ArrayList<>(list1.size() + list2.size());
        int i = 0, j = 0;

        while (i < list1.size() && j < list2.size()) {
            if (compare(list1.get(i), list2.get(j)) <= 0) {
                output.add(list1.get(i++));
            } else {
                output.add(list2.get(j++));
            }
        }

        while (i < list1.size()) {
            output.add(list1.get(i++));
        }
        while (j < list2.size()) {
            output.add(list2.get(j++));
        }

        return output;
    }

    private List<T> mergeThreeLists(List<T> list1, List<T> list2, List<T> list3) {
        int i = 0, j = 0, k = 0;
        int size1 = list1.size();
        int size2 = list2.size();
        int size3 = list3.size();

        List<T> output = new ArrayList<>(size1 + size2 + size3);

        while (i < size1 && j < size2 && k < size3) {
            T val1 = list1.get(i);
            T val2 = list2.get(j);
            T val3 = list3.get(k);

            if (compare(val1, val2) <= 0 && compare(val1, val3) <= 0) {
                output.add(val1);
                i++;
            } else if (compare(val2, val1) <= 0 && compare(val2, val3) <= 0) {
                output.add(val2);
                j++;
            } else {
                output.add(val3);
                k++;
            }
        }

        // Resztę dorzucamy za pomocą mergeTwoLists
        if (i == size1) {
            output.addAll(mergeTwoLists(list2.subList(j, size2), list3.subList(k, size3)));
        } else if (j == size2) {
            output.addAll(mergeTwoLists(list1.subList(i, size1), list3.subList(k, size3)));
        } else if (k == size3) {
            output.addAll(mergeTwoLists(list1.subList(i, size1), list2.subList(j, size2)));
        }

        return output;
    }
}

