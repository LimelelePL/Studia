import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.TreeSet;

class lab8 {
  
  static void printAll(Object... elems ){
    for (Object e : elems) {
      if (e != null) {
      System.out.println(e.getClass().getSimpleName()+ ": " + e);
      } else System.out.println("uwaga! null");
    }
  }

  public static void main(String []args) {
    printAll(1,4,"D", "3.13");
    System.out.println();
    printAll(null, new Integer[] {1,2,3,4} , new ArrayList<>(), new LinkedList<>(), new TreeSet<>() );
    System.out.println();
    printAll();
  }
}
