package zadanie1;

public class Main {
    public static void main(String[] args) throws IStack.FullStackException {
        VTS<Integer> vts = new VTS<>();
        vts.push(1);
        vts.push(2);
        vts.push(3);
        vts.push(4);
        vts.push(5);
        vts.push(6);
        vts.push(7);

        System.out.println(vts.peek());
        vts.down();
        vts.down();
        vts.down();
        vts.down();
        vts.down();

        System.out.println();
        System.out.println(vts.peek());

        System.out.println();
        vts.printStack();

    }


}
