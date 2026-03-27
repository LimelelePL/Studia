import scala.util.control.TailCalls.TailRec
object cw6 extends App {
    def whileLoop[A] (condition : A => Boolean, expression: A=>A, initialState : A) : A = {
        def loop(state : A) : A = {
            if (condition(state)) {
                val newState = expression(state)
                loop(newState)
            } else state
        }
        loop(initialState)
    }

    def swap(tab : Array[Int], i : Int, j : Int) : Unit = {
        val pom = tab(i)
        tab (i) = tab (j)
        tab (j) = pom
    }

    def choosePivot(tab : Array[Int], i : Int, j : Int) : Int = tab ( (i+j)/2 )

    def partition(tab : Array[Int], l : Int, r : Int): (Int, Int) = {
        var i = l
        var j = r
        val pivot = choosePivot(tab, l,r)

        while (i <= j) {
            while (tab(i) < pivot){ 
                i = i+1;
            }
            while (pivot < tab(j)){
                j = j - 1;
            }
            if (i <= j) {
                 swap(tab, i, j)
                 i = i+1
                 j = j-1
            }
        }
        (i,j)
    }

    def quick (tab : Array[Int], l : Int, r : Int) : Unit= {
        if (l < r) {
            val (i,j) = partition(tab, l, r)
            if (j-l < r - i) {
                 quick(tab, l ,j)
                 quick(tab, i, r)
            }
            else {
                quick(tab, i, r)
                quick(tab, l, j)
            }
        }
        else ()
    }

    def quicksort (tab : Array[Int]): Unit = quick (tab, 0, (tab.length-1))
}
