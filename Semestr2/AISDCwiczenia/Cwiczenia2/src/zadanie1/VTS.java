package zadanie1;

import java.util.NoSuchElementException;

public class VTS<E> implements IStack<E> {
    private Node<E> top;
    private int size;
    private Node<E> current;

    public VTS() {
        top = null;
        size = 0;
    }

    private static class Node<E>{
        E value;
        Node<E> next;

        public Node(E value){
            this.value = value;
        }
    }

    public E peek(){
    return current.value;
    }

    public void down(){
        if(current != null){
            current = current.next;
        } else {
            throw new NoSuchElementException();
        }
    }
    public void up(){
        if(isEmpty()){
            throw new NoSuchElementException();
        }
        current = top;
    }

    @Override
    public boolean isEmpty() {
        return size == 0;
    }

    @Override
    public boolean isFull() {
        return false;
    }

    @Override
    public E pop() throws EmptyStackException {
        if (isEmpty()) {
            throw new EmptyStackException();
        }

        Node<E> node = top;
        top = top.next;
        node.next = null;
        size--;

        current=top;
        return node.value;
    }

    @Override
    public void push(E elem) throws FullStackException {
        Node<E> node=new Node<>(elem);
        if (!isEmpty()) {
            node.next = top;
        }
        top=node;
        current=top;
        size++;
    }

    @Override
    public int size() {
        return size;
    }

    @Override
    public E top() throws EmptyStackException {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        return top.value;
    }

    public void printStack(){
        Node<E> node=top;
        while(node!=null){
            System.out.println(node.value + " ");
            node=node.next;
        }
    }
}
