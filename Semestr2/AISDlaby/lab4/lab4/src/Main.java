public class Main {
    public static void main(String[] args) {
       TwoWayLinkedList<Integer> list = new TwoWayLinkedList<>();

     for(int i=0; i<14; i++) {
           list.add(i);
       }
        list.printList();

        System.out.println();

        System.out.println("pobieram element na indeksie 5");
        System.out.println(list.get(5));


        System.out.println("Dodaje null na indeks 5");
        list.add(5,null);
        list.printList();

        System.out.println();
        System.out.println("indeks 6-stki");
        System.out.println(list.indexOf(6));

        System.out.println("usuwam element na indeksie 3 ");
        System.out.println(list.remove(3));
        list.printList();

        list.getPrev(9);

       // System.out.println("pusta lista ");
        //list.clear();
        //list.get(2);
    }
}