package zadanie6;

import java.util.Iterator;
import java.util.NoSuchElementException;

public class Iterator6 <T>implements Iterator <T> {
   private T arr[];
   private int pos=0;
   private int lastReturned=-1;

   public Iterator6(T[] arr) {
       this.arr=arr;
   }

    @Override
    public boolean hasNext() {
        return pos<arr.length;
    }

    @Override
    public T next() {
        if (!hasNext()) throw new NoSuchElementException();
        lastReturned=pos;
        return arr[pos++];
    }

    @Override
    public void remove() {
        if(lastReturned==-1) throw new IllegalStateException();

        for(int i=lastReturned; i< arr.length-1; i++){
            arr[i]=arr[i+1];
        }

        arr[arr.length-1]=null;
        lastReturned=-1;
    }
}
