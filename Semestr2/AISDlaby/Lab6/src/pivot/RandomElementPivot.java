package pivot;

import java.util.List;
import java.util.Random;

public class RandomElementPivot <T> implements PivotStrategy<T>{
    private int idx=0;
    @Override
    public T selectPivot(List<T> list, int low, int high) {
        Random rand = new Random();
        idx=rand.nextInt(high - low + 1)+low;
        return list.get(idx);
    }

    @Override
    public int getIndex() {
        return idx;
    }
}
