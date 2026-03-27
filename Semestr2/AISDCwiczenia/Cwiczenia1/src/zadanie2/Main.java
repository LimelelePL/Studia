package zadanie2;

import java.util.Iterator;

public class Main {
    public static void main(String[] args) {
        Iterator<Integer> iterator = new Iterator2(5, Integer.MAX_VALUE);
        while(iterator.hasNext()) {
            System.out.print(iterator.next() + " ");
        }
    }
}
