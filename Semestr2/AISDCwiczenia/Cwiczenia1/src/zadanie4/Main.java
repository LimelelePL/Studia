package zadanie4;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;

public class Main {
    public static void main(String[] args) {
        ArrayList<String> l1= new ArrayList<>(Arrays.asList("a", "b", "c", "d", "e", "f", "g", "h"));
        Iterator<String> it1 = l1.iterator();
        ArrayList<String> l2= new ArrayList<>(Arrays.asList("A", "B", "C", "D", "E", "F", "G", "H", "QEWR", "Erewr"));
        Iterator<String> it2 = l2.iterator();

        Iterator<String> it = new Iterator4<>(it1, it2);
        while (it.hasNext()) {
            System.out.print(it.next() + " ");
        }

    }
}
