package zadanie2;

import java.util.Iterator;

public class Iterator2 implements Iterator<Integer> {
    private int n;
    private int max;

    public Iterator2(int n, int max) {
        this.n = n;
        this.max = max;
    }

    @Override
    public boolean hasNext() {
        return n<=max;
    }

    @Override
    public Integer next() {
        return n++;
    }
}
