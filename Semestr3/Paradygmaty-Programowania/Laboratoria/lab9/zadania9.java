import java.util.Arrays;
import java.util.Comparator;

class zadania9 {

    static <T>T[] duplicate(T[] arr1, Integer [] arr2) {
        
        int resSize = 0;
        int initialSize = Math.min(arr1.length, arr2.length);

        for(int i = 0; i<initialSize; i++) {
            if (arr2[i] < 0) throw new IllegalArgumentException("wartosc ujemna");
            resSize += arr2[i];
        }

        @SuppressWarnings("unchecked")
        T[] res = (T[])new Object[resSize];

        int idx= 0;
        for (int i = 0; i<initialSize; i++) {
            int reps = arr2[i];
            for (int  j = 0; j<reps; j++) {
                res[idx++] = arr1[i];
            }
        }
        return res;
    }

    static <T> T[] add(T[] arr1, T elem, Comparator<? super T> comp){

        int idx = 0;
        @SuppressWarnings("unchecked")
        T[] res = (T[])new Object[arr1.length+1];

        while (idx < arr1.length && comp.compare(elem, arr1[idx])>0) {
            res[idx] = arr1[idx];
            idx++;
        }
        
        res[idx] = elem;

        for (int i = idx; i<arr1.length; i++) {
            res[i+1] = arr1[i];
        }

        return res;
    }
    public static void main (String[] args) {

        Object[] arr = duplicate(new Integer[]{1,2,3}, new Integer[]{0,3,4});
        System.err.println(Arrays.toString(arr));

        Comparator<Integer> comp = Comparator.naturalOrder();
        Object[] arr1 = add(new Integer[]{1,2,3,7,11,12}, 8, comp);
        System.out.println(Arrays.toString(arr1));
    }
  
}
