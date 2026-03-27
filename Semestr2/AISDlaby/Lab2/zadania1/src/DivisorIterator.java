import java.util.Iterator;
import java.util.NoSuchElementException;

public class DivisorIterator implements Iterator<Integer> {
    private final int N;
    private int divisor = 1;

    public DivisorIterator(int N) {
        if (N <= 0) {
            throw new IllegalArgumentException("N musi być liczbą dodatnią.");
        }
        this.N = N;
    }

    @Override
    public boolean hasNext() {
        return divisor <= N;
    }

    @Override
    public Integer next() {
        if (!hasNext()) {
            throw new NoSuchElementException();
        }

        while (N % divisor != 0){
            divisor++;
        }

        return divisor++;
    }

    static class DivisionIterable implements Iterable<Integer> {
        private int N;

        public DivisionIterable(int N) {
            this.N = N;
        }

        @Override
        public Iterator<Integer> iterator() {
            return new DivisorIterator(N);
        }
    }

    public static void main(String[] args) {
        int N=15;

        DivisorIterator iterator = new DivisorIterator(N);
       for (int n: new DivisionIterable(N)){
           System.out.print(n + " ");
       }
    }
}