package zadanie3;

import java.util.Iterator;

public class Main {
    public static void main(String[] args) {
        Iterator<Integer> iterator = new FibonacciGenerator();
        int count=0;
        while (iterator.hasNext() && count<10) {
            System.out.print(iterator.next() + " ");
            count++;
        }
    }
}