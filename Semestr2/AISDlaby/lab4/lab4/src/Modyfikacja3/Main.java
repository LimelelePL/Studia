package Modyfikacja3;

public class Main {
    public static void main(String[] args) {
        TwoWayCycledListWithSentinel<Integer> list = new TwoWayCycledListWithSentinel<>();
        nieparzysta(list);
        System.out.println();
        parzysta(list);
        System.out.println();
        pusta(list);
        System.out.println();
        nulle(list);
    }

    public static void nieparzysta(TwoWayCycledListWithSentinel<Integer> list){
        System.out.println("nieparzysta");
        for (int i=1; i<10; i++){
            list.add(i);
        }
        list.printList();
        System.out.println();
        System.out.println(list.middlew());
    }
    public static void parzysta(TwoWayCycledListWithSentinel<Integer> list){
        System.out.println("parzysta");
        list.add(1);
        list.printList();
        System.out.println();
        System.out.println(list.middlew());
    }

    public static void pusta(TwoWayCycledListWithSentinel<Integer> list){
        System.out.println("pusta");
        list.clear();
        System.out.println(list.middlew());
    }

    public static void nulle(TwoWayCycledListWithSentinel<Integer> list){
        System.out.println("nulle");
        for (int i=1; i<10; i++){
            list.add(null);
        }
        list.printList();
        System.out.println();
        System.out.println(list.middlew());
    }

}
