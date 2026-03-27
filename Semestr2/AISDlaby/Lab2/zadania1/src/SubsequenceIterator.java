import java.util.Iterator;
import java.util.NoSuchElementException;

public class SubsequenceIterator<T> implements Iterator <Iterator<T>> {
    private final T[] arr;
    private int currentLength;
    private int startIndex;

    public SubsequenceIterator(T[] arr) {
        this.arr=arr;
        this.currentLength=1;
        this.startIndex=0;
    }

    @Override
    public boolean hasNext() {
        return currentLength <= arr.length;
    }

    @Override
    public Iterator<T> next() {
        if (!hasNext()) {
            throw new NoSuchElementException("Brak kolejnych podciągów");
        }

        @SuppressWarnings("unchecked")
        T[] substring = (T[]) new Object[currentLength];
        for (int i=0; i<currentLength; i++) {
            substring[i]= arr[startIndex+i];
        }

        startIndex++;
        if (startIndex> arr.length-currentLength) {
            currentLength++;
            startIndex=0;

        }

        return new ArrayIterator<>(substring);
    }

}
