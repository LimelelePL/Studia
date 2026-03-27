import java.util.Iterator;
public class Mainsubsequence {
    public static void main(String[] args) {
        Integer[] arr = {1,2,3,4,5};
        SubsequenceIterator<Integer> subsequenceIterator = new SubsequenceIterator<>(arr);

        int index=0;
        while (subsequenceIterator.hasNext()) {
            System.out.print("i" + index + ": ");
            Iterator<Integer> subIterator = subsequenceIterator.next();
            while (subIterator.hasNext()) {
                System.out.print(subIterator.next() + " ");
            }
            System.out.println();
            index++;
        }
    }
}
