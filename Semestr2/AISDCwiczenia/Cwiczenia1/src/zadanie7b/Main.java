package zadanie7b;
import java.util.Iterator;

public class Main {
    public static void main(String[] args) {
        Integer [][]arr= {{1,2,3}, {1,2}, {1,4,5}};
        Iterator<Integer> it = new Iterator7b<>(arr);

        while(it.hasNext()) {
            System.out.print(it.next()+ " ");
        }
    }
}
