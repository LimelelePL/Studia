package zadanie1;
/*
Zaimplementuj iterator, który przyjmie inny iterator jako bazowy i zwróci każdy k-ty element
z kolekcji.
 */

import java.util.Iterator;
import java.util.NoSuchElementException;

public class Iterator1<T> implements Iterator<T> {
    private final Iterator<T> it;
    private final int k;
    private int index=0;
    private T current;

    public Iterator1(Iterator<T> it, int k) {
        this.it = it;
        this.k = k;
        findNextValid();
    }

    public void findNextValid(){
        while(it.hasNext()){
            T elem = it.next();
            index++;
            if(index%k==0){
                current = elem;
                return;
            }
        }
        current = null;
    }

    @Override
    public boolean hasNext(){
        return current!=null;
    }

    @Override
    public T next() {
        if(!hasNext()){
            throw new NoSuchElementException();
        }
        T value=current;
        findNextValid();
        return value;
    }
}
