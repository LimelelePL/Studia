import java.util.NoSuchElementException;

public class TwoWayLinkedList <E> implements IList<E> {
    private Node<E> head;
    private Node<E> tail;
    private int size;
    private Node<E> header;
    private Node<E> trail;
    private Node<E> beforeHeader;

    public TwoWayLinkedList() {
        size = 0;
        beforeHeader = new Node<>(null);
        header = new Node<>(null);
        trail = new Node<>(null);

        beforeHeader.next = header;
        header.prev = null;
        header.next = trail;
        trail.prev = beforeHeader;

        head = null;
        tail = null;
    }

   private static class Node<E>{
        E value;
        Node<E> next;
        Node<E> prev;

        public Node(E value) {
            this.value = value;
        }
    }

    public boolean addFirst(E e) {
        Node<E> newNode = new Node<>(e);
        if(size==0){
            header.next = newNode;
            newNode.prev = beforeHeader;
            newNode.next = trail;
            trail.prev = header;
            tail=newNode;
            head = newNode;
        } else {
            header.next = newNode;
            newNode.prev = head.prev;
            head.prev = header;
            head.next.prev = newNode;
            newNode.next = head;
            head=newNode;

            if (size==1){
                trail.prev=newNode;
            }
        }
        size++;
        return true;
    }

    @Override
    public boolean add(E e) {
        Node<E> newNode = new Node<>(e);
        if(size == 0){
           addFirst(e);
        } else{
            tail.next = newNode;
            newNode.prev = trail.prev;
            newNode.next=trail;
            tail=newNode;
            trail.prev = tail.prev.next;
        }
        size++;
        return true;
    }

    @Override
    public void add(int index, E element) {
        if(index<0 || index>size){
            throw new IndexOutOfBoundsException();
        }
        if(index==0){
            addFirst(element);
            return;
        }
        if(index==size){
            add(element);
            return;
        }

        Node<E> tempPrev = getNode(index-1);
        Node<E> tempAdvance = tempPrev.next;

        Node<E> node = new Node<>(element);

        node.next = tempAdvance;
        node.prev = tempAdvance.prev;
        tempPrev.next = node;
        tempAdvance.prev = tempPrev;
        tempAdvance.next.prev = node;

        size++;
    }

    @Override
    public void clear() {
        head = null;
        tail = null;
        size = 0;

        beforeHeader.next = header;
        header.prev = null;
        header.next = trail;
        trail.prev = beforeHeader;
    }

    @Override
    public boolean contains(E element) {
        return getNode(indexOf(element))!=null;
    }

    @Override
    public E get(int index) {
        return (E) getNode(index).value;
    }

    @Override
    public E set(int index, E element) {
        getNode(index).value = element;
        return (E) getNode(index).value;
    }

    @Override
    public int indexOf(E element) {
       Node <E> node=head;

       int idx=0;
       while (node!=trail){
           if((node.value==element)){
               return idx;
           }
           idx++;
           node=node.next;
       }
        throw new NoSuchElementException();
    }

    @Override
    public boolean isEmpty() {
        return size==0;
    }

    public E removeLast(){
        if(size<=1){
            return removeFirst();
        }
        Node <E> temp=tail;
        Node <E> prev=trail.prev;
        prev.next=trail;
        trail.prev=tail.prev;
        tail=prev;

       return temp.value;
    }

    public E removeFirst(){
        if (size==0){
            throw new NoSuchElementException();
        }
        if (size==1){
            Node<E> node=head;
            clear();
            return node.value;
        }

        Node <E> temp=head;
        head=head.next;
        header.next=head;
        head.prev=beforeHeader;
        head.next.prev=header;

        return temp.value;
    }

    // 1 2 3 4 5
    @Override
    public E remove(int index) {
        if(index<0 || index>=size){
            throw new IndexOutOfBoundsException();
        }
        if(index==size-1){
           return removeLast();
        }
        if((index == 0) || (size <= 1)){
            return removeFirst();
        }

        Node<E> previous=getNode(index-1);
        Node <E> node=previous.next;
        Node<E> advance=node.next;

        previous.next = advance;
        advance.prev = node.prev;
        advance.next.prev = previous;

        node.next=null;
        node.prev=null;

        size--;

        return node.value;
    }

    @Override
    public boolean remove(E element) {
        remove(indexOf(element));
        return true;
    }

    @Override
    public int size() {
        return size;
    }

    public Node<E> getNode(int index) {
        if (index < 0 || index >= size || isEmpty()) {
            throw new IndexOutOfBoundsException("Indeks poza zakresem lub pusta lista ");
        }
        if (index == size - 1) {
            return tail;
        }

        Node<E> current = head;
        for (int i = 0; i < index; i++) {
            current = current.next;
        }
        return current;
    }

    public void getPrev(int index) {
        Node<E> node=getNode(index);
        System.out.println();
        System.out.println("wczesniejszy element " + node.value+ " to " + node.prev.value);
    }

    public void printList(){
        if(isEmpty()){
            throw new NoSuchElementException("pusta lista");
        }

        Node<E> current=head;
        while (current!=trail){
            System.out.print(current.value+ " ");
            current=current.next;
        }
    }

}