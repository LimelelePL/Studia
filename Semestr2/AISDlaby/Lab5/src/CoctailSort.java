import core.AbstractSwappingSortingAlgorithm;

import java.util.Comparator;
import java.util.List;

public class CoctailSort<T> extends AbstractSwappingSortingAlgorithm<T> {
    public CoctailSort(Comparator<? super T> comparator) {
        super(comparator);
    }

    @Override
    public List<T> sort(List<T> list) {
        int left=0;
        int right=list.size()-1;
        boolean swapped=true;

        while(swapped) {
            swapped=false;

            for(int i=left; i<right; i++){
               if( compare(list.get(i), list.get(i+1)) >0 ){
                   swap(list, i, i+1);
                   swapped=true;
               }
            }
            right--;
            for(int i=right; i>left; i--){
                if( compare(list.get(i), list.get(i-1)) <0 ){
                    swap(list, i, i-1);
                    swapped=true;
                }
            }
            left++;
        }
        return list;
    }
}
