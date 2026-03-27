import java.util.*;

public class MaxBinomialHeap<T> implements IHeap<T> {
    private final LinkedList<Node<T>> rootList;
    private final Comparator<T> comparator;

    public MaxBinomialHeap(Comparator<T> comparator) {
        if (comparator == null) {
            throw new IllegalArgumentException("Comparator cannot be null");
        }
        this.comparator = comparator;
        this.rootList = new LinkedList<>();
    }

    private static class Node<T> {
        private T value;
        private Node<T> leftChild;
        private Node<T> sibling;
        private Node<T> parent;
        private int degree;

        public Node(T value) {
            this.value = value;
            this.leftChild = null;
            this.sibling = null;
            this.parent = null;
            this.degree = 0;
        }
    }

    @Override
    public T maximum() {
        if (rootList.isEmpty()) {
            throw new NoSuchElementException("Heap is empty");
        }
        Node<T> maxNode = Collections.max(rootList, Comparator.comparing(node -> node.value, comparator));
        return maxNode.value;
    }

    @Override
    public T deleteMaximum() {
        if (rootList.isEmpty()) {
            throw new NoSuchElementException("Heap is empty");
        }
        // usuwamy najwiekszy element z rootlist
        Node<T> maxNode = Collections.max(rootList, Comparator.comparing(node -> node.value, comparator));
        rootList.remove(maxNode);

        // dodajemy do pomocniczej listy wszystkie dzieci tego elementu
        LinkedList<Node<T>> children = new LinkedList<>();
        Node<T> child = maxNode.leftChild;
        while (child != null) {
            Node<T> nextChild = child.sibling;
            child.sibling = null;
            child.parent = null;
            children.addFirst(child);
            child = nextChild;
        }

        // laczymy pomocnicza liste z obecna rootlist tworzac nowy kopiec
        MaxBinomialHeap<T> aux = new MaxBinomialHeap<>(comparator);
        aux.rootList.addAll(children);
        this.merge(aux);

        return maxNode.value;
    }

    @Override
    public void insert(T x) {
        if (x == null) {
            throw new IllegalArgumentException("Element cannot be null");
        }
        Node<T> newNode = new Node<>(x);
        MaxBinomialHeap<T> singleNodeHeap = new MaxBinomialHeap<>(comparator);
        singleNodeHeap.rootList.add(newNode);
        this.merge(singleNodeHeap);
    }

    @Override
    public void merge(MaxBinomialHeap<T> other) {
        if (other == null || other.rootList.isEmpty()) return;
        if (this.rootList.isEmpty()) {
            this.rootList.addAll(other.rootList);
            return;
        }

        LinkedList<Node<T>> merged = mergeLists(this.rootList, other.rootList);
        this.rootList.clear();

        // idziemy po 3 korzeniach na raz i laczymy je w pary
        Iterator<Node<T>> it = merged.iterator();
        Node<T> x = it.hasNext() ? it.next() : null;
        Node<T> y = it.hasNext() ? it.next() : null;
        Node<T> z = it.hasNext() ? it.next() : null;

        while (x != null) {
            // 1) x nie da sie polaczc z innym drzewem
            if (y == null || x.degree < y.degree) {
                this.rootList.add(x);
                x = y;
                y = z;
                z = it.hasNext() ? it.next() : null;
            }
            // 2) 3 te same stopnie drew nie scalamy x i y bo by powstal konflikt
            else if (z != null && x.degree == y.degree && y.degree == z.degree) {
                this.rootList.add(x);
                x = y;
                y = z;
                z = it.hasNext() ? it.next() : null;
            }
            // 3) 2 te same stopnie drzewa i 3 inny ktory nie spowoduje konfliktu np 2,2,3
            else {
                Node<T> mergedTree;
                if (comparator.compare(x.value, y.value) >= 0) {
                    y.parent = x;
                    y.sibling = x.leftChild;
                    x.leftChild = y;
                    x.degree++;
                    mergedTree = x;
                } else {
                    x.parent = y;
                    x.sibling = y.leftChild;
                    y.leftChild = x;
                    y.degree++;
                    mergedTree = y;
                }
                x = mergedTree;
                y = z;
                z = it.hasNext() ? it.next() : null;
            }
        }
    }

    private LinkedList<Node<T>> mergeLists(LinkedList<Node<T>> ll1, LinkedList<Node<T>> ll2) {
        LinkedList<Node<T>> merged = new LinkedList<>();
        Iterator<Node<T>> it1 = ll1.iterator();
        Iterator<Node<T>> it2 = ll2.iterator();

        Node<T> n1 = it1.hasNext() ? it1.next() : null;
        Node<T> n2 = it2.hasNext() ? it2.next() : null;

        while (n1 != null && n2 != null) {
            if (n1.degree <= n2.degree) {
                merged.add(n1);
                n1 = it1.hasNext() ? it1.next() : null;
            } else {
                merged.add(n2);
                n2 = it2.hasNext() ? it2.next() : null;
            }
        }
        while (n1 != null) {
            merged.add(n1);
            n1 = it1.hasNext() ? it1.next() : null;
        }
        while (n2 != null) {
            merged.add(n2);
            n2 = it2.hasNext() ? it2.next() : null;
        }
        return merged;
    }

    public void printBFS() {
        for (Node<T> root : rootList) {
            LinkedList<Node<T>> queue = new LinkedList<>();
            queue.add(root);
            while (!queue.isEmpty()) {
                Node<T> node = queue.poll();
                System.out.print(node.value + " ");
                Node<T> child = node.leftChild;
                while (child != null) {
                    queue.add(child);
                    child = child.sibling;
                }
            }
        }
        System.out.println();
    }
}
