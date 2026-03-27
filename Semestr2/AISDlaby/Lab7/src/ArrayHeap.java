import java.util.ArrayList;
import java.util.Comparator;
import java.util.NoSuchElementException;

public class ArrayHeap <T> extends TreeArrayBinaryHeap<T>  implements HeapInterface<T>{
    private final ArrayList<T> heap;
    private final Comparator<? super T> comparator;

    public ArrayHeap (Comparator<? super T> comparator1) {
        super(comparator1);
        this.comparator = comparator1;
        heap = new ArrayList<>();
    }

    public ArrayHeap(ArrayHeap<T> other,Comparator<? super T> comparator) {
        super(comparator);
        this.heap = new ArrayList<>(other.heap);
        this.comparator = comparator;
    }


    @Override
    public String toString() {
        return heap.toString();
    }

    @Override
    public void add(T item) {
        addToArrayHeap(item);
    }

    @Override
    public T maximum() {
        return maxFromArrayHeap();
    }

    @Override
    public void clear() {
        clearArrayHeap();
    }

    public T peek() {
        if (heap.isEmpty()) throw new NoSuchElementException("Heap is empty");
        return heap.get(0);
    }

    private boolean hasRightChild(int index) {
        return 2 * index + 2 < heap.size();
    }

    private boolean hasLeftChild(int index) {
        return 2 * index + 1 < heap.size();
    }

    private void addToArrayHeap(T value) {
        heap.add(value);
        int index = heap.size() - 1;

        while (index > 0) {
            int parentIndex = getParentIndex(index);

            if( getComparator().compare(heap.get(parentIndex),heap.get(index))< 0) {
                T tmp = heap.get(index);
                heap.set(index, heap.get(parentIndex));
                heap.set(parentIndex, tmp);

                index = parentIndex;
            } else {
                break;
            }
        }
    }

    private T maxFromArrayHeap() {
        if (heap.isEmpty()) {
            throw new NoSuchElementException("Heap is empty");
        }

        if (heap.size() == 1) {
            return heap.removeFirst();
        }

        T max = heap.getFirst();
        heap.set(0, heap.removeLast());

        int index=0;
        while (hasLeftChild(index)) {

            int largest = index;
            int leftChildIndex = getLeftChildIndex(index);
            int rightChildIndex = getRightChildIndex(index);

            if(leftChildIndex< heap.size() &&
                  getComparator().compare( heap.get(leftChildIndex),(heap.get(largest))) > 0){

                largest = leftChildIndex;
            }
            if(rightChildIndex< heap.size() &&
                    getComparator().compare(heap.get(rightChildIndex) , heap.get(largest)) > 0){

                largest = rightChildIndex;
            }
            if (largest != index) {
                T temp = heap.get(index);
                heap.set(index, heap.get(largest));
                heap.set(largest, temp);
                index = largest;
            } else {
                break;
            }
        }
        return max;
    }

    private void clearArrayHeap() {
        heap.clear();
    }
    public boolean isEmpty() {
        return heap.isEmpty();
    }

    public ArrayList<T> getHeap() {
        return heap;
    }
    public int getHeight(){
        return (int) (Math.log(heap.size() + 1) / Math.log(2));
    }

}
