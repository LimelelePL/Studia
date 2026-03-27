public class Stack<E> implements IStack<E> {
    private Node<E> top;
    private int size;

    public Stack() {
        top = null;
        size = 0;
    }

    static class Node<E> {
        E value;
        Node<E> next;

        public Node(E value) {
            this.value = value;
        }
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

        return node.value;
    }

    @Override
    public void push(E elem) throws FullStackException {
        Node<E> node = new Node<>(elem);
        if (!isEmpty()) {
            node.next = top;
        }
        top = node;
        size++;
    }

    @Override
    public int size() {
        return size;
    }

    @Override
    public E top() throws EmptyStackException {
        if(isEmpty()) {
            throw new EmptyStackException();
        }
        return top.value;
    }

    public void printStack() {
        Node<E> node = top;
        while (node != null) {
            System.out.println(node.value + " ");
            node = node.next;
        }
    }

    private void insertAtBottom(E element) throws EmptyStackException, FullStackException {
        Stack<E> temp = new Stack<>();

        while (!this.isEmpty()) {
            temp.push(this.pop());
        }

        this.push(element);

        while (!temp.isEmpty()) {
            this.push(temp.pop());
        }
    }
//1234-4321

    public void reverse() throws EmptyStackException, FullStackException {
        Stack<E> tempStack = new Stack<>();

        while (!this.isEmpty()) {
            tempStack.push(this.pop());
        }

        while (!tempStack.isEmpty()) {
            E element = tempStack.pop();
           insertAtBottom(element);
        }
    }

}
