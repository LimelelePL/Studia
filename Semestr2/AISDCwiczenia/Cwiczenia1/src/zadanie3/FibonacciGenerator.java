package zadanie3;

import java.util.Iterator;

public class FibonacciGenerator implements Iterator<Integer> {
    private int a = 0;
    private int b = 1;

    @Override
    public boolean hasNext() {
        return true;
    }

    @Override
    public Integer next() {
        int c=a+b;
        a=b;
        b=c;

        return a;
    }
}
