public interface TrieOperations <V> {
    V insert(String key, V value);
    V search(String key);
    V delete(String key);
}
