package zadanie4;
 @SuppressWarnings("unchecked")
public class DrowningStackb<E> implements IStack<E>{
    private static final int DEFAULT_CAPACITY = 16;
    private E[] array;
    private int topIndex;
    private int downIndex;
    private int size;
    private int capacity;

    public DrowningStackb(int capacity ) {
        this.capacity = capacity;
        array = (E[]) new Object[capacity + 1];
        topIndex=0;
        downIndex=0;
        size=0;
    }

    public DrowningStackb() {
        this(DEFAULT_CAPACITY);
    }

    @Override
    public boolean isEmpty() {
        return size==0;
    }

    @Override
    public boolean isFull() {
        return size == capacity;
    }

    @Override
    public E pop() throws EmptyStackException {
        if(isEmpty()) throw new EmptyStackException();

        topIndex = (topIndex - 1 + capacity) % capacity;
        E value = array[topIndex];
        size--;
        return value;
    }


    @Override
    public void push(E elem) throws FullStackException {
        if(size==capacity){
            downIndex=(downIndex+1)%capacity;
        } else {
            size++;
        }
        array[topIndex] = elem;
        topIndex = (topIndex + 1) % capacity;
    }

    @Override
    public int size() {
        return size;
    }

    @Override
    public E top() throws EmptyStackException {
        if (isEmpty())
            throw new EmptyStackException();

        return array[topIndex - 1];
    }

    public void printStack() {
        if (isEmpty()) {
            System.out.println("Stos jest pusty.");
            return;
        }

        System.out.println("Zawartość stosu (od dołu do góry):");
        int index = downIndex;
        for (int i = 0; i < size; i++) {
            System.out.println(array[index]);
            index = (index + 1) % capacity;
        }
    }
}
