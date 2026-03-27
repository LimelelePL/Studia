import java.util.*;

public class TreeArrayBinaryHeap<T> implements HeapInterface<T> {
    private int maxHeight;
    private TreeNode root;
    private int size;
    private final Comparator<? super T> comparator;

    public TreeArrayBinaryHeap(int maxHeight, Comparator<T> comparator) {
        this.comparator = comparator;
        this.maxHeight = maxHeight;
        if(maxHeight < 0){
            throw new IllegalArgumentException("Max height musi byc dodatnia");
        }
        size = 0;
    }

    public TreeArrayBinaryHeap(Comparator<? super T> comparator) {
        this.comparator = comparator;
    }

    public class TreeNode {
        private TreeNode left;
        private TreeNode right;
        private T value;
        private ArrayHeap<T> subHeapLeft, subHeapRight;

        public TreeNode(T value) {
            this.value = value;
        }
    }
    @Override
    public void add(T item) {
        if (size < fullTreeCapacity()) {
            addToTree(item);
        } else {
            addToSubheaps(item);
        }
        size++;
    }

    @Override
    public T maximum() {
        if (size == 0) throw new NoSuchElementException();

        if (size == 1) {
            T elem = root.value;
            root = null;
            size = 0;
            return elem;
        }

        // zastąpujemy root ostatnim elementem (z drzewa lub podkopca)
        T result = root.value;
        T lastVal = replaceRootWithLast();
        root.value = lastVal;
        size--;

        // heapify w drzewie i w ewentualnych podkopcach, w przypadku jak root ma 2 subkopce
        heapifyDownTree();
        heapifyDownSubheaps(root);

        return result;
    }

    @Override
    public void clear() {
        root = null;
        size = 0;
    }


///////////////////////////////////////////////////////////////////////////////////////////////////////

    //modyfikacja
    public void remove(T element){
        if(size==0) throw new NoSuchElementException(" heap is empty");

        List<T> removedElements= new ArrayList<>();
        boolean removed=false;

        while(size>0){
            T max=maximum();
            if(!removed && max.equals(element)){
                removed=true;
            } else {
                removedElements.add(max);
            }
        }
        if(!removed){
            throw new NoSuchElementException(" cannot find the element " + element);
        }

        for (T elem: removedElements) {
            add(elem);
        }
    }
//modyfiakcja

    private void reorderAfterAdd(int leafIndex, boolean leftSide) {
        TreeNode node = getNode(leafIndex);
        ArrayHeap<T> heap = leftSide ? node.subHeapLeft : node.subHeapRight;

        // jezeli max z podkopca jest mniejszy od rodzica z drzewa to robimy reorder
        T subMax = heap.peek();
        if (comparator.compare(subMax,node.value) <= 0) {
            return;
        }
        heap.maximum();

        //zamieniamy najwiekszy element z heapa z mniejszym z drzewa
        T old = node.value;
        node.value = subMax;

        heap.add(old);

        //heapify up na drzewie
        int currentIdx = leafIndex;
        TreeNode current = node;
        while (currentIdx > 0) {
            int parentIdx = getParentIndex(currentIdx);
            TreeNode parent = getNode(parentIdx);
            if (comparator.compare(parent.value,current.value) < 0) {
                swapValues(parent, current);
                currentIdx = parentIdx;
                current = parent;
            } else {
                break;
            }
        }
    }


    private void addToSubheaps(T item) {
        int h = maxHeight;
        int firstIdx = (int)Math.pow(2, h) - 1;       // indeks pierwszego węzła na poziomie Hmax
        int lastIdx = (int) Math.pow(2, h+1) - 2; // indeks ostatniego węzła na poziomie Hmax
        int actualEnd = Math.min(lastIdx, size - 1);

        //zbieram do listy wezly które są na poziomie maxHeight i robie dla nich podkopce
        ArrayList<TreeNode> maxHeightNodes = new ArrayList<>();
        for (int i = firstIdx; i <= actualEnd; i++) {
            TreeNode node = getNode(i);
            if (node.subHeapLeft == null) {
                node.subHeapLeft = new ArrayHeap<T>(comparator);
            }
            if (node.subHeapRight == null) {
                node.subHeapRight = new ArrayHeap<>(comparator);
            }
            maxHeightNodes.add(node);
        }

        // minimalna wysokosc wsrod podkopców
        int minHeight = 100000;
        for (TreeNode node : maxHeightNodes) {
            minHeight = Math.min(minHeight, node.subHeapLeft.getHeight());
            minHeight = Math.min(minHeight, node.subHeapRight.getHeight());
        }

        //dodajemy element do kopcja o najmniejszej ilosci elemenotw
        for (int i = 0; i < maxHeightNodes.size(); i++) {
            TreeNode node = maxHeightNodes.get(i);
            int idx = firstIdx + i;
            if (node.subHeapLeft.getHeight() == minHeight) {
                node.subHeapLeft.add(item);
                reorderAfterAdd(idx, true);
                break;
            }
            if (node.subHeapRight.getHeight() == minHeight) {
                node.subHeapRight.add(item);
                reorderAfterAdd(idx, false);
                break;
            }
        }

    }

    private void swapValues(TreeNode a, TreeNode b) {
        T tmp = a.value;
        a.value = b.value;
        b.value = tmp;
    }

    private TreeNode getNode(int index) {
        if (size == 0) throw new NoSuchElementException();
        if (index < 0 || index >= size) throw new IndexOutOfBoundsException();
        if (index == 0) return root;

        ArrayList<Integer> path = calculateTrack(index);
        TreeNode node = root;

        for (int i = path.size() - 1; i >= 0; i--) {
            if (path.get(i) == 0) {
                node = node.left;
            } else {
                node = node.right;
            }
            if (node == null)
                throw new NoSuchElementException("Drzewo ma niepełną gałąź");
        }
        return node;
    }

    private ArrayList<Integer> calculateTrack(int index) {
        ArrayList<Integer> binaryRepresentation = new ArrayList<>();
        int k = index + 1;
        while (k > 1) {
            binaryRepresentation.add(k % 2);
            k /= 2;
        }
        return binaryRepresentation;
    }

    private int fullTreeCapacity() {
        return (int)Math.pow(2, maxHeight+1) - 1;
    }

    private T replaceRootWithLast() {
        if (size <= fullTreeCapacity()) {
            return replaceRootFromTree();
        } else {
            return replaceRootFromSubheaps();
        }
    }

    private T replaceRootFromSubheaps() {
        List<Integer> bits = calculateTrack(size - 1);
        Collections.reverse(bits);

        TreeNode parent = descend(bits.subList(0, maxHeight));

        boolean isLeft = (bits.get(maxHeight) == 0);

        ArrayHeap<T> heap;
        if (isLeft) {
            heap = parent.subHeapLeft;
        } else {
            heap = parent.subHeapRight;
        }

        return heap.maximum();
    }

    //zejscie na dol do ostatniego nodea
    private TreeNode descend(List<Integer> bits) {
        TreeNode node = root;
        for (int b : bits) {
            if(b==0){
                node = node.left;
            } else{
                node = node.right;
            }
        }
        return node;
    }

    private T replaceRootFromTree() {
        TreeNode last = getNode(size - 1);
        T val = last.value;
        removeLastTreeNode();
        return val;
    }

    private void removeLastTreeNode() {
        int lastIndex = size - 1;
        if (lastIndex == 0) {
            root = null;
            return;
        }
        int p = getParentIndex(lastIndex);
        TreeNode parent = getNode(p);
        if (getLeftChildIndex(p) == lastIndex) {
            parent.left = null;
        } else {
            parent.right = null;
        }
    }


    private void heapifyDownTree() {
        TreeNode cur = root;
        int lvl = 0;
        while (lvl < maxHeight && cur.left != null) {
            TreeNode bigger = pickBiggerChild(cur);
            if (comparator.compare(bigger.value,cur.value) > 0) {
                swapValues(cur, bigger);
                cur = bigger;
                lvl++;
            } else {
                return;
            }
        }
    }

    private TreeNode pickBiggerChild(TreeNode node) {
        if (node.right == null) {
            return node.left;
        }

        if (comparator.compare(node.left.value,node.right.value) >= 0) {
            return node.left;
        } else {
            return node.right;
        }

    }

    private void heapifyDownSubheaps(TreeNode cur) {
        ArrayHeap<T> L = cur.subHeapLeft;
        ArrayHeap<T> R = cur.subHeapRight;

        //wybieramy z ostatnich dwóch subheaps najwiekszy element
        T leftMax=null;
        if(L != null && !L.isEmpty()) {
            leftMax = L.peek();
        }

        T rightMax=null;
        if(R != null && !R.isEmpty()) {
            rightMax = R.peek();
        }

        // zamieniamy elementy
        if (leftMax != null && (rightMax == null || comparator.compare(leftMax,(rightMax)) >= 0)
                && comparator.compare(leftMax,cur.value) > 0) {
            T old = cur.value;
            T newValue = L.maximum();
            cur.value = newValue;
            L.add(old);

        } else if (rightMax != null &&comparator.compare( rightMax,(cur.value)) > 0) {
            T old = cur.value;
            T newValue = R.maximum();
            cur.value = newValue;
            R.add(old);
        }
    }

    private void addToTree(T value) {
        TreeNode newNode = new TreeNode(value);
        if (size == 0) {
            root = newNode;
            return;
        }
        //sciezka binarna
        List<Integer> path = calculateTrack(size);
        Collections.reverse(path);

        //zbieram wezly wedlug sciezki
        List<TreeNode> nodes = new ArrayList<>();
        TreeNode cur = root;
        nodes.add(cur);

        for (int i = 0; i < path.size() - 1; i++) {
            if(path.get(i) == 0) {
                cur=cur.left;
            } else {
                cur = cur.right;
            }
            nodes.add(cur);
        }

        //dodajemy element na koniec w odpowiednie moejsce
        if (path.getLast() == 0) {
            cur.left = newNode;
        } else {
            cur.right = newNode;
        }
        nodes.add(newNode);
        //heapify up
        heapifyUp(nodes);
    }

    private void heapifyUp(List<TreeNode> path) {
        for (int i = path.size() - 1; i > 0; i--) {
            TreeNode child = path.get(i);
            TreeNode parent = path.get(i - 1);
            if (comparator.compare(parent.value,(child.value)) < 0) {
                swapValues(parent, child);
            } else {
                break;
            }
        }
    }

    private int getMaxHeight() {
        return maxHeight;
    }

    protected int getParentIndex(int index) {
        return (index - 1) / 2;
    }

    protected int getLeftChildIndex(int index) {
        return (index * 2) + 1;
    }

    protected int getRightChildIndex(int index) {
        return (index * 2) + 2;
    }

    public void printHeapWithSubheaps() {
        //  Drzewiasta część:
        System.out.print("Tree: ");
        int treeCap = fullTreeCapacity();
        for (int i = 0; i < size && i < treeCap; i++) {
            System.out.print(getNode(i).value + " ");
        }
        System.out.println();

        // Jeżeli nie ma jeszcze żadnych podkopców, wychodzimy:
        if (size <= treeCap) {
            return;
        }

        //  Zakres liści w drzewiastej części (już mamy przynajmniej jeden pełny poziom):
        int firstLeaf = (1 << maxHeight) - 1;
        int lastLeaf  = Math.min(size - 1, treeCap - 1);

        //  Dla każdego liścia wypisz tylko te subkopce, które istnieją:
        System.out.println("Subheaps at leaves:");
        for (int i = firstLeaf; i <= lastLeaf; i++) {
            TreeNode leaf = getNode(i);
            boolean hasLeft  = leaf.subHeapLeft  != null && !leaf.subHeapLeft.isEmpty();
            boolean hasRight = leaf.subHeapRight != null && !leaf.subHeapRight.isEmpty();

            if (!hasLeft && !hasRight)
                continue;   // pomijamy liście, które nie mają subkopców

            System.out.print("Leaf[" + i + "]=" + leaf.value);
            if (hasLeft) {
                System.out.print("  L-sub: " + heapToString(leaf.subHeapLeft));
            }
            if (hasRight) {
                System.out.print("  R-sub: " + heapToString(leaf.subHeapRight));
            }
            System.out.println();
        }
    }

    private String heapToString(ArrayHeap<T> heap) {
        ArrayHeap<T> copy = new ArrayHeap<>(heap,comparator);
        List<T> elems = new ArrayList<>();
        while (!copy.isEmpty()) {
            elems.add(copy.maximum());
        }
        return elems.toString();
    }
    public Comparator<? super T> getComparator() {
        return comparator;
    }
}
