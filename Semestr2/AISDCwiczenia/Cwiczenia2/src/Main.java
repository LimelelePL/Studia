public class Main {
    public static void main(String[] args) throws IStack.EmptyStackException, IStack.FullStackException {
       Stack<String> s = new Stack<>();

       s.push("A");
       s.push("B");
       s.push("C");

       System.out.println("PRZED:");
       s.printStack();
       System.out.println();

       s.reverse();

       System.out.println("PO:");
       s.printStack();
    }
}