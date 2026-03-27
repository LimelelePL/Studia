package zadanie4;

import java.util.Iterator;
import java.util.NoSuchElementException;

public class Iterator4 <T> implements Iterator<T> {
    private Iterator<T> it1;
    private Iterator<T> it2;
    private boolean shuffled = true;


    public Iterator4(Iterator<T> it1, Iterator<T> it2) {
        this.it1 = it1;
        this.it2 = it2;
    }

    @Override
    public boolean hasNext() {
        return (it1.hasNext() || it2.hasNext());
    }

    @Override
    public T next() {
        if(!hasNext()){
            throw new NoSuchElementException();
        }

        T result;

        if(shuffled && it1.hasNext()) {
            result = it1.next();
        }
        else if(!shuffled && it2.hasNext()) {
            result = it2.next();
        }
        else if(it1.hasNext()){
            result = it1.next();
        }
        else {
            result = it2.next();
        }

        shuffled = !shuffled;

        return result;

    }
}
