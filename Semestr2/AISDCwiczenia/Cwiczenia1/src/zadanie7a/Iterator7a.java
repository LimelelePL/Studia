package zadanie7a;

import java.util.Iterator;
import java.util.NoSuchElementException;

public class Iterator7a<T> implements Iterator<T> {
    private T[][] arr;
    private int currentRow;
    private int currentCol;

    public Iterator7a(T[][] arr) {
        this.arr = arr;
        currentRow = 0;
        currentCol = 0;
        getToNextRow();
    }

    public void getToNextRow() {
        while (currentRow < arr.length && currentCol >= arr[currentRow].length) {
            currentRow++;
            currentCol = 0;
        }
    }

    public boolean isEnd() {
        return currentRow >= arr.length;
    }

        @Override
        public boolean hasNext () {
            return !isEnd();
        }

        @Override
        public T next () {
            if (!hasNext()) {
                throw new NoSuchElementException();
            }
            T value = arr[currentRow][currentCol];
            currentCol++;
            getToNextRow();
            return value;
        }
}
