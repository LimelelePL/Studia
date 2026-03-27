package zadanie5b;

import java.util.Iterator;
import java.util.NoSuchElementException;

public class Iterator5b implements Iterator <Integer> {
    private int n;
    private int nextPrime;
    private int current = 1;

    public Iterator5b(int n) {
        this.n = n;
        advance();
    }

    private void advance() {
        nextPrime = -1;
        for (int i = current + 1; i <= n; i++) {
            if (isPrime(i)) {
                nextPrime = i;
                break;
            }
        }
    }

    private boolean isPrime(int num) {
        if (num < 2) return false;

        for (int j = 2; j <= num - 1; j++) {
            if (num % j == 0) {
                return false;
            }
        }
        return true;
    }

    @Override
    public boolean hasNext() {
        return nextPrime != -1;
    }

    @Override
    public Integer next() {
        if (!hasNext()) throw new NoSuchElementException();
        int result = nextPrime;
        advance();
        return result;
    }
}
