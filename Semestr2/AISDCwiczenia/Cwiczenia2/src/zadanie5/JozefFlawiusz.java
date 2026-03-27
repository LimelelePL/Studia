package zadanie5;

import zadanie3.IQueue;
import zadanie3.QueueOfStacks;

public class JozefFlawiusz {

    public static int flawiusz(int n, int k) throws IQueue.EmptyQueueException {
        QueueOfStacks<Integer> queue = new QueueOfStacks<>();

        for (int i = 1; i <= n; i++) {
            queue.enqueue(i);
        }
        queue.printQueue();
        while (queue.size() > 1) {
            for (int i = 1; i < k; i++) {
                queue.enqueue(queue.dequeue());
            }
            queue.dequeue();
        }

        return queue.dequeue();
    }

    public static void main(String[] args) throws IQueue.EmptyQueueException {
        int f= flawiusz(8,3);
        System.out.println(f);
    }

}
