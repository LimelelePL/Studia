package pivot;

import java.util.List;

public class FirstElementPivot <T> implements PivotStrategy<T>{
    private int idx=0;
    @Override
    public T selectPivot(List<T> list, int low, int high) {
        idx=low;
        return list.get(low);
    }

    @Override
    public int getIndex() {
        return idx;
    }

}
