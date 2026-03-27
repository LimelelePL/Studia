package pivot;

import java.util.List;

public interface PivotStrategy <T>{
    T selectPivot(List<T> list, int low, int high);
    int getIndex();
}
