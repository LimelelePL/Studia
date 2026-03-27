public interface IHeap<T> {
    T maximum();
    T deleteMaximum();
    void insert(T x);
    void merge(MaxBinomialHeap<T> heap2);
}
