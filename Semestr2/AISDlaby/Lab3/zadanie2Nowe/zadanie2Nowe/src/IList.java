
    public interface IList<T>{
        boolean add(T e); // dodanie elementu na koniec listy
        void add(int index, T element); // dodanie elementu na podanej pozycji
        void clear(); // skasowanie wszystkich elementów
        boolean contains(T element); // czy lista zawiera podany element (equals())
        T get(int index); // pobranie elementu z podanej pozycji
        T set(int index, T element); // ustawienie nowej wartości na pozycji
        int indexOf(T element); // pozycja szukanego elementu (equals())
        boolean isEmpty(); // czy lista jest pusta
        T remove(int index); // usuwa element z podanej pozycji
        boolean remove(T element); // usuwa element (equals())
        int size(); // rozmiar listy
    }
