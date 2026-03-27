package zadanie5a;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.NoSuchElementException;

public class Iterator5a implements Iterator <Integer> {
    private final ArrayList<Integer> primeNumbers = new ArrayList<>();
    private final int n;
    private int index =0;

    public Iterator5a(int n) {
        this.n = n;
        addPrimeNumbers();
    }

    public boolean isPrime(int number) {
        if (number <2) return false;
        for (int i = 2; i <= number -1; i++) {
            if (number % i == 0) {
                return false;
            }
        }
        return true;
    }

    public void addPrimeNumbers(){
        int number=1;
        while(number<=n){
            if (isPrime(number)){
                primeNumbers.add(number);
            }
            number++;
        }
    }

    @Override
    public boolean hasNext() {
        return index < primeNumbers.size();
    }

    @Override
    public Integer next() {
        if (!hasNext()) throw new NoSuchElementException();
        return primeNumbers.get(index++);
    }
}
