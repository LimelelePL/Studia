package zadanie3;

import java.util.Queue;
import java.util.Stack;

public class QueueOfStacks <T> implements IQueue<T> {
    private Stack<T> inStack = new Stack<>();
    private Stack<T> outStack = new Stack<>();

    @Override
    public boolean isEmpty() {
        return inStack.isEmpty() && outStack.isEmpty();
    }

    @Override
    public boolean isFull() {
        return false;
    }

    @Override
    public T dequeue() throws EmptyQueueException {
        if (isEmpty()) {
            throw new EmptyQueueException();
        }
        if (outStack.isEmpty()) {
            moveInToOut();
        }
        return outStack.pop();
    }

    @Override
    public void enqueue(T elem) {
        inStack.push(elem);
    }

    private void moveInToOut() {
        while (!inStack.isEmpty()) {
            outStack.push(inStack.pop());
        }
    }


    @Override
    public int size() {
        return inStack.size() + outStack.size();
    }

    @Override
    public T first() throws EmptyQueueException {
        if (isEmpty()) {
            throw new EmptyQueueException();
        }
        if (outStack.isEmpty()) {
            moveInToOut();
        }
        return outStack.peek();
    }

    public void printQueue() {
        if (isEmpty()) {
            return;
        }


        @SuppressWarnings("unchecked")
        Stack<T> tempOut = (Stack<T>) outStack.clone();
        while (!tempOut.isEmpty()) {
            System.out.print(tempOut.pop() + " ");
        }

        @SuppressWarnings("unchecked")
        T[] inArray = (T[]) inStack.toArray();
        for (int i = 0; i < inArray.length; i++) {
            System.out.print(inArray[i] + " ");
        }

        System.out.println();
    }
}
