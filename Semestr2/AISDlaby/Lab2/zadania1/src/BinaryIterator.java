import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.NoSuchElementException;

public class BinaryIterator implements Iterator<Integer> {
    private Iterator<Integer> it;
    ArrayList<Integer> list;

    public BinaryIterator(Iterator<Integer> it) {
        this.it = it;
        list=new ArrayList<>();
    }

    public void calculateToBinary(int n){
        if (n < 0) {
            throw new IllegalArgumentException("BinaryIterator nie obsługuje liczb ujemnych: ");
        }
        list = new ArrayList<>();

        if(n==0){
            list.add(0);
        }
        while (n > 0) {
            if (n % 2 == 0) {
                list.add(0);
            } else {
                list.add(1);
            }
            n/=2;
        }
    }

    @Override
    public boolean hasNext() {
        return !list.isEmpty() || it.hasNext();
    }

    @Override
    public Integer next() {
        int value;

        if (!hasNext()) {
            throw new NoSuchElementException();
        }

        if (list.isEmpty()) {
            calculateToBinary(it.next());
        }

        value=list.getLast();
        list.removeLast();

        return value;
    }

    public static void main(String[] args) {
    ArrayList<Integer> list = new ArrayList<>(Arrays.asList(0,1,2,3,4,5));
    BinaryIterator it = new BinaryIterator(list.iterator());
    while (it.hasNext()) {
        System.out.print(it.next()+ " ");
        }
    }

}
