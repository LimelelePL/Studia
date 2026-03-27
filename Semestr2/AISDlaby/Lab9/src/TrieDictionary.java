import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class TrieDictionary <V> implements TrieOperations<V> {
    private TrieNode<V> root;
    private final Comparator<Character> comparator;

    public TrieDictionary(Comparator<Character> comparator) {
        this.root = new TrieNode<>('\0');
        this.comparator = comparator;
    }

    private static class TrieNode<V>{
        private V value;
        private char key;
        private TrieNode<V> firstChild;
        private TrieNode<V> nextSibling;

        public TrieNode(char key){
            this.key = key;
            this.value=null;
            this.firstChild = null;
            this.nextSibling = null;
        }
    }

    public List<String> suggest(String prefix){

        TrieNode<V> node=root;
        if (node==null) return new ArrayList<>();

        for (int i=0; i<prefix.length(); i++){
            char ch=prefix.charAt(i);
            node=findChildNode(node,ch);
        }

        return suggest(node, new StringBuilder(prefix));
    }

    private List<String> suggest(TrieNode<V> node, StringBuilder prefix){
        List<String> results=new ArrayList<>();
        if(node==null) return results;
        if(node.value!=null){
            results.add(prefix.toString());
        }
        TrieNode<V> child=node.firstChild;
        while (child!=null){
            prefix.append(child.key);
            results.addAll(suggest(child, prefix));
            prefix.setLength(prefix.length()-1);
            child=child.nextSibling;
        }
        return results;
    }


    @Override
    public V insert(String key, V value) {
        if (key == null) {
            throw new IllegalArgumentException("Klucz nie może być null.");
        }
        if (key.isEmpty()) {
            throw new IllegalArgumentException("Klucz nie może być pusty.");
        }
        if (value == null) {
            throw new IllegalArgumentException("Wartość nie może być null.");
        }

        TrieNode<V> currentNode = root;
        for (int i = 0; i < key.length(); i++) {
            char ch = key.charAt(i);
            TrieNode<V> child = findChildNode(currentNode, ch);
            if (child == null) {
                child = addChildNode(currentNode, ch);
            }
            currentNode = child;
        }

        V oldValue = currentNode.value;
        currentNode.value = value;
        return oldValue;
    }

    private TrieNode<V> addChildNode(TrieNode<V> parentNode, char ch) {
        TrieNode<V> newChild = new TrieNode<>(ch);
        TrieNode<V> prev = null;
        TrieNode<V> current = parentNode.firstChild;

        // miejsce do wstawienia węzła w porządku leksykograficznym
        while (current != null && comparator.compare(current.key,ch)<0) {
            prev = current;
            current = current.nextSibling;
        }

        if (prev == null) {
            // Wstaw na początek listy dzieci
            newChild.nextSibling = parentNode.firstChild;
            parentNode.firstChild = newChild;
        } else {
            // Wstaw pomiędzy prev a current
            newChild.nextSibling = current;
            prev.nextSibling = newChild;
        }
        return newChild;
    }

    @Override
    public V search(String key) {
        if (key == null) {
            throw new IllegalArgumentException("Klucz nie może być null.");
        }
        if (key.isEmpty()) {
            return null;
        }

        TrieNode<V> currentNode = root;
        for (int i = 0; i < key.length(); i++) {
            char ch = key.charAt(i);

            TrieNode<V> child = findChildNode(currentNode, ch);
            if (child == null) {
                return null;
            }
            currentNode = child;
        }
        return currentNode.value;
    }

    @Override
    public V delete(String key) {
        if (key == null) {
            throw new IllegalArgumentException("Klucz nie może być null.");
        }
        if (key.isEmpty()) {
            return null;
        }

        // Ścieżka węzłów od korzenia do węzła docelowego
        List<TrieNode<V>> path = new ArrayList<>();
        TrieNode<V> currentNode = root;
        path.add(currentNode);

        for (int i = 0; i < key.length(); i++) {
            char ch = key.charAt(i);
            TrieNode<V> child = findChildNode(currentNode, ch);
            if (child == null) {
                return null;
            }
            currentNode = child;
            path.add(currentNode);
        }

        // currentNode to teraz węzeł dla ostatniego znaku klucza
        if (currentNode.value == null) {
            return null;
        }

        V valueToRemove = currentNode.value;
        currentNode.value = null; // "nie-klucz"

        // Węzeł jest zbędny tzn .value == null oraz .firstChild == null
        for (int i = path.size() - 1; i > 0; i--) {
            TrieNode<V> nodeToPotentiallyRemove = path.get(i);
            TrieNode<V> parentOfNode = path.get(i - 1);

            if (nodeToPotentiallyRemove.value == null && nodeToPotentiallyRemove.firstChild == null) {
                // Usuwamy nodeToPotentiallyRemove z listy dzieci parentOfNode
                removeChildNode(parentOfNode, nodeToPotentiallyRemove.key);
            } else {
                break;
            }
        }
        return valueToRemove;
    }
    private TrieNode<V> findChildNode(TrieNode<V> parentNode, char ch) {
        TrieNode<V> currentChild = parentNode.firstChild;
        while (currentChild != null) {
            if (comparator.compare(currentChild.key,ch)==0) {
                return currentChild;
            }
            currentChild = currentChild.nextSibling;
        }
        return null;
    }

    private void removeChildNode(TrieNode<V> parentNode, char ch) {
        TrieNode<V> currentChild = parentNode.firstChild;
        TrieNode<V> prevChild = null;

        while (currentChild != null) {
            if (comparator.compare(currentChild.key,ch)==0) {
                // Znaleziono dziecko do usunięcia
                if (prevChild == null) { // Jest to pierwsze dziecko na liście rodzeństwa
                    parentNode.firstChild = currentChild.nextSibling;
                } else {
                    prevChild.nextSibling = currentChild.nextSibling;
                }
                return;
            }
            prevChild = currentChild;
            currentChild = currentChild.nextSibling;
        }
    }

    public void printAllKeysDfs() {
        System.out.println("Klucze w słowniku (DFS):");
        dfsPrint(root.firstChild, new StringBuilder());
    }

    private void dfsPrint(TrieNode<V> currentNode, StringBuilder currentPath) {
        if (currentNode == null) {
            return;
        }
        currentPath.append(currentNode.key);
        if (currentNode.value != null) {
            System.out.println(currentPath.toString() + ": " + currentNode.value);
        }
        dfsPrint(currentNode.firstChild, currentPath);
        currentPath.setLength(currentPath.length() - 1);
        dfsPrint(currentNode.nextSibling, currentPath);
    }
}
