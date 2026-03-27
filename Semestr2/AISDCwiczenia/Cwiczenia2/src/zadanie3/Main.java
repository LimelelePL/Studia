package zadanie3;

public class Main {
    public static void main(String[] args) throws IQueue.FullQueueException, IQueue.EmptyQueueException {
        QueueOfStacks<Integer> q = new QueueOfStacks<>();
        q.enqueue(1);
        q.enqueue(2);
        q.enqueue(3);
        q.enqueue(4);


        q.printQueue();
        q.dequeue();
        System.out.println();
        q.printQueue();

        System.out.println();
        System.out.println(q.first());
    }
}
