package zadanie6;

import java.util.Iterator;

public class Main {
    public static void main(String[] args) {
        Integer[] tab={1,2,3,4,5,6};

        Iterator<Integer> iterator6 = new Iterator6<>(tab);
        System.out.println(iterator6.next());
        System.out.println(iterator6.next());

        iterator6.remove();

        while(iterator6.hasNext()){
            System.out.println(iterator6.next());
        }
    }
}
