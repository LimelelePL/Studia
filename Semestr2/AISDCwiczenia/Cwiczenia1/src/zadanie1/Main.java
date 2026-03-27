package zadanie1;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;

public class Main {
    public static void main(String[] args) {
        ArrayList<Integer> list = new ArrayList<>(Arrays.asList(1,2,3,4,5,6,7,8,9));
        Iterator<Integer> iterator1= new Iterator1<>(list.iterator(),4);
        while(iterator1.hasNext()){
            System.out.println(iterator1.next());
        }
    }
}
