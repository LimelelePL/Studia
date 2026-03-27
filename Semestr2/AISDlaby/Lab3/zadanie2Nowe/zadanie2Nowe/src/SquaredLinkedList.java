import java.util.ArrayList;

public class SquaredLinkedList <T> implements IList<T> {
    private RowNode<T> head;
    private int size;
    private int K;

    public SquaredLinkedList() {
        head = null;
        size = 0;
        K = 0;
    }

    static class Node<T> {
        T value;
        Node<T> next;

        public Node(T value) {
            this.value = value;
            next = null;
        }

        public Node(T value, Node<T> next) {
            this.value = value;
            this.next = next;
        }

    }

    static class RowNode<T>{
        RowNode<T> nextRow;
        Node<T> head;
        int rowSize;

        public RowNode() {
            head =null;
            nextRow = null;
            rowSize = 0;
        }
    }

    public void calculateNewK(){
        int newK = (int) Math.floor(Math.sqrt(size));
        K=newK;
    }

    public ArrayList<Node<T>> makeListFlat(){

        RowNode<T> row = head;
        ArrayList<Node<T>> list = new ArrayList<>();

        while (row!=null){
                Node<T> col=row.head;
                while (col != null) {
                    list.add(col);
                    col = col.next;
            }
            row=row.nextRow;
        }
        return list;
    }

    public void resizeToBiggerSquare(ArrayList<Node<T>> list) {
        calculateNewK();





    }

    @Override
    public boolean add(T e) {
        if(isEmpty()){

            Node<T> node=new Node(e);
            RowNode<T> row=new RowNode<>();
            row.head=node;

            size++;
            K=1;
            return true;
        }
        return true;
    }

    @Override
    public void add(int index, T element) {

    }

    @Override
    public void clear() {
        size = 0;
        head = null;
        K=0;
    }

    @Override
    public boolean contains(T element) {
        return false;
    }

    @Override
    public T get(int index) {
        return null;
    }

    @Override
    public int indexOf(T element) {
        return 0;
    }

    @Override
    public boolean isEmpty() {
        return size == 0;
    }

    @Override
    public boolean remove(T element) {
        return false;
    }

    @Override
    public T remove(int index) {
        return null;
    }

    @Override
    public T set(int index, T element) {
        return null;
    }

    @Override
    public int size() {
        return size;
    }
}
