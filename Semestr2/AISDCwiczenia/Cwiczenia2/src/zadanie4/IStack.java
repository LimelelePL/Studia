package zadanie4;

public interface IStack<T>{
    public class EmptyStackException extends Exception{
    }
    public class FullStackException extends Exception{
    }
        boolean isEmpty();
        boolean isFull();
        T pop() throws EmptyStackException;
        void push(T elem) throws FullStackException;
        int size(); // zwraca liczbę elementów na stosie
        T top() throws EmptyStackException;
// zwraca element ze szczytu stosu bez usuwania go
    }
