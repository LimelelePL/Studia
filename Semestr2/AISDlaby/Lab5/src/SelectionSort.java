import core.AbstractSwappingSortingAlgorithm;

import java.util.Comparator;
import java.util.List;

public class SelectionSort<T> extends AbstractSwappingSortingAlgorithm<T> {

    public SelectionSort(Comparator<? super T> comparator) {
        super(comparator);
    }

    @Override
    public List<T> sort(List<T> list) {
        int size = list.size();
        for(int i=size-1; i>=0; i--) {
            int maxIndex = i;
            for(int j=i-1; j>=0; j--) {
              if(compare(list.get(j), list.get(maxIndex)) > 0) {
                  maxIndex = j;
              }
            }
            if(maxIndex != i) {
                swap(list, i, maxIndex);
            }
        }

        return list;
    }
}
