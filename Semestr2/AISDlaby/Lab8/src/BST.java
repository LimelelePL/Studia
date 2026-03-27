import java.util.Comparator;
import java.util.NoSuchElementException;

public class BST<T> {
    private Node<T> root;
    private Comparator<T> comparator;


    public BST(Comparator<T> comparator) {
        root = null;
        this.comparator = comparator;
    }

    public boolean rContains(T value){
        return rContains(root, value);
    }

    private boolean rContains(Node<T> node, T value) {
        if (node == null) return false;

        int cmp = comparator.compare(value, node.getValue());
        if (cmp == 0) {
            return true;
        } else if (cmp < 0) {
            return rContains(node.getLeft(), value);
        } else {
            return rContains(node.getRight(), value);
        }
    }

    public boolean insert(T value){
        if(value==null) throw new IllegalArgumentException("nie mozna wstawic nulla");
        Node<T> newNode=new Node<>(value);
        if(root==null){
            root = newNode;
            return true;
        }
        Node<T> temp=root;
        while(true){
            if(comparator.compare(value, temp.getValue())==0){
                return false;
            }
            if(comparator.compare(value, temp.getValue())<0){
                if(temp.getLeft()==null){
                    temp.setLeft(newNode);
                    return true;
                }
                temp=temp.getLeft();
            } else{
                if(temp.getRight()==null){
                    temp.setRight(newNode);
                    return true;
                }
                temp=temp.getRight();
            }
        }
    }
    public T successor(T value){
        if(root==null) throw new NoSuchElementException();
        if(!rContains(value)) throw new NoSuchElementException();

        Node<T> temp=root;
        Node<T> successor=null;

        //znalezienie elemetu
        while(temp!=null){
            int cmp = comparator.compare(value, temp.getValue());
            if(cmp<0){
                successor=temp; //potencjalny nastepnik
                temp=temp.getLeft();
            } else if(cmp>0){
                temp=temp.getRight();
            } else break;
        }

        //szukamy nastepnika najpierw w prawym podrzwie,
        // a nastepnie w najnizszym elemencie lewej galezi drzewa
        if (temp != null && temp.getRight() != null) {
            Node<T> temp1 = temp.getRight();
            while (temp1.getLeft() != null) {
                temp1 = temp1.getLeft();
            }
            successor = temp1;
        }

        if(successor==null) throw new NoSuchElementException("brak nastepnika");
        return successor.getValue();
    }

    public T delete(T value) {
        if (root == null) throw new NoSuchElementException();

        Node<T> current = root;
        Node<T> parent = null;

        //szukamy wezla i jego rodzica
        while (current != null && comparator.compare(value, current.getValue()) != 0) {
            parent = current;
            int cmp = comparator.compare(value, current.getValue());
            if (cmp < 0) {
                current = current.getLeft();
            } else current = current.getRight();
        }

        if (current == null) throw new NoSuchElementException("Brak takiego elementu w drzewie");

        //lisc
        if (current.getLeft() == null && current.getRight() == null) {
            if (current == root) {
                root = null;
            } else if (parent.getLeft() == current) {
                parent.setLeft(null);
            } else {
                parent.setRight(null);
            }
        }//jedno dziecko
        else if (current.getLeft() == null || current.getRight() == null) {
            Node<T> child = (current.getLeft() != null) ? current.getLeft() : current.getRight();

            if (current == root) {
                root = child;
            } else if (parent.getLeft() == current) {
                parent.setLeft(child);
            } else {
                parent.setRight(child);
            }
        }
        //dwoje dzieci
        else {
            Node<T> successorParent = current;
            Node<T> successor = current.getRight();

            while (successor.getLeft() != null) {
                successorParent = successor;
                successor = successor.getLeft();
            }

            current.setValue(successor.getValue());

            if (successorParent.getLeft() == successor) {
                successorParent.setLeft(successor.getRight());
            } else {
                successorParent.setRight(successor.getRight());
            }
        }

        return value;
    }

    public T findMin() {
        if (root == null) throw new NoSuchElementException();
        return findMin(root);
    }

    private T findMin(Node<T> node) {
       if(node==null) return null;

       if(node.getLeft()!=null){
           return findMin(node.getLeft());
       }

       return node.getValue();
    }

    public T findMax() {
        if (root == null) {
            throw new NoSuchElementException();
        }
        return findMax(root);
    }

    private T findMax(Node<T> node) {
        if (node == null) return null;

        if(node.getRight()!=null){
            return findMax(node.getRight());
        }
        return node.getValue();
    }

    public T kthBiggest(int k){
        return kthBiggest(k,root, new Counter());
    }

    private T kthBiggest(int k, Node<T> node, Counter counter){
        if(node==null) return null;

        T right=kthBiggest(k,node.getRight(), counter);
        if(right!=null) {
            return right;
        }
        counter.count++;
        if(counter.count==k){
            return node.getValue();
        }
        return kthBiggest(k,node.getLeft(), counter);
    }

    private static class Counter{
        int count=0;
    }

    public <R> void preOrderWalk(IExecutor<T, R> exec) {
        preOrderWalk(root, exec);
    }

    private <R> void preOrderWalk(Node<T> node, IExecutor<T, R> exec) {
        if (node != null) {
            exec.execute(node.getValue());
            preOrderWalk(node.getLeft(), exec);
            preOrderWalk(node.getRight(), exec);
        }
    }

}
