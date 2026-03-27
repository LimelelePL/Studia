public class Main {
    public static void main(String[] args) {

            OneWaySquareList<Integer> list = new OneWaySquareList<>();
            System.out.println("== Pusta lista ==");
            list.print();

            for (int i = 1; i <= 19; i++) {
                list.add(i);
                System.out.println("== Po wstawieniu wartości " + i + " ==");
                list.print();
            }
        System.out.println("==wstawiam Nulla na indeks 2 ==");
            list.add(2,null);
            list.print();

        System.out.println("Pobieram wartość o indeksie 3");
        System.out.println(list.get(3).toString());
        System.out.println("Pobieram indeks nulla");
        System.out.println(list.indexOf(null));
        System.out.println("zamieniam element o indeksie 1");
        System.out.println(list.set(1,12).toString());
        list.print();
        System.out.println("Usuwam element o indeksie 2");
        list.remove(2);
        list.print();


        System.out.println();
        list.print();

        int middle= list.middlew();
        System.out.println(middle);

        }
    }