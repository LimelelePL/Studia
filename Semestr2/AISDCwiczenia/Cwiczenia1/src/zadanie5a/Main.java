package zadanie5a;

import java.util.Iterator;

public class Main {
    public static void main(String[] args) {
        Iterator<Integer> iterator = new Iterator5a(100);
        while (iterator.hasNext()) {
            System.out.print(iterator.next()+  " ");
        }
    }
}
