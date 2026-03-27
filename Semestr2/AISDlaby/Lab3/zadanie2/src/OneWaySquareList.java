import java.util.Arrays;
import java.util.NoSuchElementException;

public class OneWaySquareList<E> implements IList<E> {
        private Node<E> head;
        private int size;
        private int k;

        private static class Node<E> {
            E value;
            Node<E> nextRow;
            Node<E> nextColumn;

            public Node(E value) {
                this.value = value;
            }
        }

        public OneWaySquareList() {
            head = null;
            size = 0;
            k = 0;
        }

        @Override
        public boolean add(E e) {
            if (isEmpty()) {
                head = new Node<>(e);
                size = 1;
                k = 1;
                return true;
            }
            // w tym przypadku trzeba zmienic kształt na wiekszy kwadrat
            if (size+1 == (k+1) * (k+1)) {

                E[] array = copyToArr();
                int newK=k+1;
                clear();
                k=newK;

                for (int i = 0; i < array.length; i++) {
                    simpleAdd(array[i]);
                }
            }
            simpleAdd(e);
            return true;
        }

    private void simpleAdd(E e) {
        Node<E> newNode = new Node<>(e);
        //na poczatku przy dodawaniu lista jest pusta, czyli ustawiamy parametry na nowo
        if (isEmpty()) {
            head = newNode;
            size = 1;
            return;
        }
        //jeszcze jest miejsce w wierszu
        if (size % k != 0) {
            Node<E> last = getLastNode();
            last.nextColumn = newNode;
            //nie ma miejsca w wierszu, trzeba dodac nowy wiersz
        } else {
            Node<E> lastInFirstCol = getLastInFirstColElem();
            lastInFirstCol.nextRow = newNode;
        }
        size++;
    }


    @Override
        public void add(int index, E element) {
            if (index < 0 || index > size) {
                throw new IndexOutOfBoundsException();
            }
            if (index == size) {
                add(element);
                return;
            }

            E[] array = copyToArr();
            //kopiujemy elementy do tablicy o 1 wiekszej i w miejscu w liscie gdzie chcemy umieścić nowy element,
            // to umieszczamy go w odpowiednim indeksie tablicy
            @SuppressWarnings("unchecked")
            E[] nextArray= (E[])new Object[array.length+1];
            nextArray[index] = element;
            for (int i = 0; i < array.length; i++) {
                if (i < index) {
                    nextArray[i] = array[i];
                } else {
                    nextArray[i+1] = array[i];
                }
            }
            //reorganizujemy liste
                int newK=k;
                if(size+1==(k+1) * (k+1)) {
                    newK=k+1;
                }

                clear();
                k=newK;

                for (int i = 0; i < nextArray.length; i++) {
                    simpleAdd(nextArray[i]);
                }
        }

        @Override
        public void clear() {
            head = null;
            size = 0;
            k = 0;
        }

        @Override
        public boolean contains(E element) {
            return indexOf(element) != -1;
        }

        @Override
        public E get(int index) {
            if (index < 0 || index >= size) {
                throw new IndexOutOfBoundsException();
            }
            int count = 0;
            Node<E> currentRow = head;
            while (currentRow != null) {
                Node<E> current = currentRow;
                while (current != null) {
                    if (count == index) {
                        return current.value;
                    }
                    count++;
                    current = current.nextColumn;
                }
                currentRow = currentRow.nextRow;
            }
            return null;
        }

    @Override
        public E set(int index, E element) {
            if(index < 0 || index >= size) {
                throw new IndexOutOfBoundsException();
            }

             Node<E> row = head;
             Node<E> col = row;
             int count=0;

             while (row != null) {
                 while (col != null) {
                     if (count == index) {
                         E prevValue=col.value;
                         col.value = element;
                         return prevValue;
                     }
                     count++;
                     col = col.nextColumn;
                 }
                 row = row.nextRow;
             }
             return null;
        }

        @Override
        public int indexOf(E element) {
            int index = 0;
            Node<E> currentRow = head;
            while (currentRow != null) {
                Node<E> current = currentRow;
                while (current != null) { //jakby element, ktorego szukamy byl nullem to i tak trzeba go zwrócic
                    if ((element==null && current.value==null) || (element!= null && element.equals(current.value))) {
                        return index;
                    }
                    index++;
                    current = current.nextColumn;
                }
                currentRow = currentRow.nextRow;
            }
            return -1;
        }

        @Override
        public boolean isEmpty() {
            return size == 0;
        }

        @Override
        public E remove(int index) {
            if (index < 0 || index >= size) {
                throw new IndexOutOfBoundsException();
            }

            E[] array = copyToArr();
            @SuppressWarnings("unchecked")
                    //kopiujemy wszystkie elementy, bez tego ktory usuwamy
            E[] nextArray= (E[])new Object[array.length-1];
            for (int i = 0; i<index; i++) {
                nextArray[i] = array[i];
            }
            for (int i=index; i<size-1; i++) {
                nextArray[i] = array[i+1];
            }

            //trzeba nowe K zaokraglic w dol przy usuowaniu\
            int newSize = size - 1;
            int newK = (int) Math.floor(Math.sqrt(newSize));

            clear();
            k = newK;

            for (int i = 0; i < nextArray.length; i++) {
                simpleAdd(nextArray[i]);
            }

            return get(index);
        }

        @Override
        public boolean remove(E element) {
            int index = indexOf(element);
            if (index != -1) {
                remove(index);
                return true;
            } else throw new NoSuchElementException();
        }

        @Override
        public int size() {
            return size;
        }

    public E[] copyToArr(){
        @SuppressWarnings("unchecked")
        E[] array = (E[]) new Object[size];
        int idx = 0;
        Node<E> row = head;
        while (row != null) {
            Node<E> col = row;
            while (col != null) {
                array[idx++] = col.value;
                col = col.nextColumn;
            }
            row = row.nextRow;
        }
        return array;
    }


    private Node<E> getLastNode() {

            Node<E> last = null;
            Node<E> currentRow = head;
            while (currentRow != null) {
                Node<E> current = currentRow;
                while (current != null) {
                    last = current;
                    current = current.nextColumn;
                }
                currentRow = currentRow.nextRow;
            }
            return last;
        }

        private Node<E> getLastInFirstColElem() {
            Node<E> current = head;
            while (current.nextRow != null) {
                current = current.nextRow;
            }
            return current;
        }

    public void print() {
        if (isEmpty()) {
            System.out.println("Lista jest pusta.");
            return;
        }

        Node<E> currentRow = head;

        while (currentRow != null) {
            Node<E> current = currentRow;
            while (current != null) {
                System.out.print("[" + current.value + "] ");
                if (current.nextColumn != null) {
                    System.out.print("-> ");
                }
                current = current.nextColumn;
            }
            System.out.println();
            currentRow = currentRow.nextRow;

        }
    }

    public E middle() {
        Node<E> slowRow = head;
        Node<E> slowCol = head;
        Node<E> fastRow = head;
        Node<E> fastCol = head;

        while (fastRow != null && fastCol != null) {
            for (int i = 0; i < 2; i++) {
                if (fastCol.nextColumn != null) {
                    fastCol = fastCol.nextColumn;
                } else {
                    fastRow = fastRow.nextRow;
                    if (fastRow != null) {
                        fastCol = fastRow;
                    }
                    else {
                        fastCol = null;
                    }
                }
            }
            if (fastCol != null) {
                if (slowCol.nextColumn != null) {
                    slowCol = slowCol.nextColumn;
                } else {
                    slowRow = slowRow.nextRow;
                    if (slowRow != null) {
                        slowCol = slowRow;
                    }
                    else {
                        slowCol = null;
                    }
                }
            }
        }
        if(slowCol!=null){
            return slowCol.value;
        } else {
            return null;
        }
    }

    public E middlew() {
        Node<E> slowRow = head;
        Node<E> slowCol = head;
        Node<E> fastRow = head;
        Node<E> fastCol = head;

        while (fastRow != null && fastCol!=null) {
            for (int i = 0; i < 2; i++) {

                if(fastCol==null){
                    break;
                }

                if (fastCol.nextColumn != null ) {
                    fastCol = fastCol.nextColumn;
                } else {
                    fastRow = fastRow.nextRow;
                    fastCol = fastRow;
                }
            }

            if (fastCol != null) {
                if (slowCol.nextColumn != null) {
                    slowCol = slowCol.nextColumn;
                } else {
                    slowRow = slowRow.nextRow;
                    slowCol = slowRow;
                }
            }
        }

        if(slowCol!=null){
            return slowCol.value;
        } else {
            return null;
        }
    }

}
