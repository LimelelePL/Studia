package zadanie5b;

import java.util.Iterator;

public class Main {
    public static void main(String[] args) {
        Iterator<Integer> it = new Iterator5b(19);

        it.next();

        while (it.hasNext()) {
            System.out.print(it.next() + " ");
       }
    }
}
