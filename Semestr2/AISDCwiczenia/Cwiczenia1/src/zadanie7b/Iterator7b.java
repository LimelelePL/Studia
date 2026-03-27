package zadanie7b;

import java.util.Iterator;
import java.util.NoSuchElementException;

public class Iterator7b<T> implements Iterator<T> {
   private T [][]arr;
   private int currentRow;
   private int currentCol;

   public Iterator7b(T [][]arr) {
       this.arr = arr;
       currentRow = arr.length-1;
       currentCol = arr[currentRow].length-1;
       moveNext();
   }

   public void moveNext(){
       while(currentRow>0 && currentCol<0){
           currentRow--;
           currentCol = arr[currentRow].length - 1;
       }
   }

    @Override
    public boolean hasNext() {
        return currentRow>=0 && currentCol>=0;
    }

    @Override
    public T next() {
       if(!hasNext()){
           throw new NoSuchElementException();
       }
       T value = arr[currentRow][currentCol];
        currentCol--;
       moveNext();
       return value;
    }
}
