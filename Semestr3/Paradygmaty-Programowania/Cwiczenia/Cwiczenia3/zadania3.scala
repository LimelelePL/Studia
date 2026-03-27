
object zadania3 extends App {
  // zad 2
  def curry3[A, B, C, D](f: ((A, B, C)) => D): A => B => C => D =
    (a: A) => (b: B) => (c: C) => f((a, b, c))

  val curry3 = [A, B, C, D] =>
    (f: ((A, B, C)) => D) => (a: A) => (b: B) => (c: C) => f((a, b, c))

  def uncurry3[A, B, C, D](f: A => B => C => D): ((A, B, C)) => D = {
    case (a, b, c) => f(a)(b)(c)
  }

  val uncurry3 = [A, B, C, D] =>
    (f: A => B => C => D) => (t: (A, B, C)) => f(t._1)(t._2)(t._3)

//zad 3
  def sumProd(xs: List[Int]): (Int, Int) = {
    xs.foldLeft((0, 1))((accum, elem) =>
      accum.match { case (a, b) => (a + elem, b * elem) }
    )
  }

  val s = sumProd(List(1, 2, 3, 4, 5))

// INSERTION SORT :( MERGE SORT KURWAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
// 1 2 1 4 9 3 ->

  def insertionSort[A](comp: (A, A) => Boolean, xs: List[A]): List[A] = {
    def insert(xs: List[A], elem: A): List[A] = xs match 
        case head :: tail =>
          if (!comp(elem, head)) elem :: xs
          else head :: insert(tail, elem)
        case Nil => List(elem)
      

    def sort(xs: List[A], sortedPart: List[A]): List[A] = xs match
      case head :: tail => sort(tail, insert(sortedPart, head))
      case Nil          => sortedPart

    sort(xs, List())
  }


  def mergeSort[A] (comp: (A, A) => Boolean, xs: List[A]): List[A] = {
    def merge (comp: (A, A) => Boolean, result: List[A], xs: List[A], ys: List[A]): List[A] = {
        (xs, ys) match
            case (h1::t1, h2::t2) =>
                 if (comp(h1, h2)|| !comp(h1,h2)) then merge(comp, h1::result, t1, ys)
                 else  merge(comp, h2::result, xs, t2)
            case ( Nil, h2::t2 ) => result.reverse ::: ys
            case ( h1::t1, Nil ) => result.reverse ::: xs
            case (Nil, Nil) => result.reverse
    }
    def partition (xs: List[A]): (List[A], List[A]) = {
        def iter (xs: List[A], fast : List[A], slow : List[A], left: List[A], right: List[A]): (List[A], List[A]) = {
            (fast, slow) match
                case (h1::a::b, h2::t2) => iter(xs, b, t2, h2::left,h2:: t2)
                case (h1::Nil, h2::t2 ) => ((left).reverse,h2:: t2)
                case (Nil, h2::t2) => ((left).reverse, h2::t2)
                case _ =>  ((left).reverse, Nil)
            } 
        iter(xs, xs , xs, Nil, Nil)
    }
    def sort (xs : List[A]) : List[A] = {
        xs match
            case Nil => Nil
            case List(_) => xs
            case _ => {
                val (a,b) = partition(xs)
                merge (comp, Nil , sort(a) , sort(b))
            }
        }
        sort(xs)
    }

   // val sortTest = mergeSort((a:Int, b:Int) => a>=b, List(3,2,3,9,1) )
    //print (sortTest.toString())


  println("1️⃣ Prosty rosnący sort:")
  println(mergeSort((a: Int, b: Int) => a < b, List(3, 1, 2)))
  println("Oczekiwane: List(1, 2, 3)\n")

  println("2️⃣ Nieparzysta liczba elementów:")
  println(mergeSort((a: Int, b: Int) => a < b, List(5, 4, 3, 2, 1)))
  println("Oczekiwane: List(1, 2, 3, 4, 5)\n")

  println("3️⃣ Parzysta liczba elementów:")
  println(mergeSort((a: Int, b: Int) => a < b, List(6, 5, 4, 3, 2, 1)))
  println("Oczekiwane: List(1, 2, 3, 4, 5, 6)\n")

  println("4️⃣ Duplikaty:")
  println(mergeSort((a: Int, b: Int) => a < b, List(3, 1, 3, 2, 3)))
  println("Oczekiwane: List(1, 2, 3, 3, 3)\n")

  println("5️⃣ Już posortowana:")
  println(mergeSort((a: Int, b: Int) => a < b, List(1, 2, 3, 4, 5)))
  println("Oczekiwane: List(1, 2, 3, 4, 5)\n")

  println("6️⃣ Odwrotne sortowanie:")
  println(mergeSort((a: Int, b: Int) => a > b, List(1, 2, 3, 4, 5)))
  println("Oczekiwane: List(5, 4, 3, 2, 1)\n")

  println("7️⃣ Dłuższa lista losowa:")
  println(mergeSort((a: Int, b: Int) => a < b, List(10, 3, 5, 1, 9, 4, 2, 8, 6, 7)))
  println("Oczekiwane: List(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)\n")

  println("8️⃣ Jednoelementowa lista:")
  println(mergeSort((a: Int, b: Int) => a < b, List(42)))
  println("Oczekiwane: List(42)\n")

  println("9️⃣ Pusta lista:")
  println(mergeSort((a: Int, b: Int) => a < b, Nil))
  println("Oczekiwane: List()\n")

  println("🔟 Ujemne i dodatnie liczby:")
  println(mergeSort((a: Int, b: Int) => a < b, List(0, -5, 3, -2, 1, -4)))
  println("Oczekiwane: List(-5, -4, -2, 0, 1, 3)\n")
}
