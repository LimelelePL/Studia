sealed trait lBT[+A]
case object LEmpty extends lBT[Nothing]
case class LNode[+A](elem: A, left: () => lBT[A], right: () => lBT[A]) extends lBT[A]

object cwiczenia5 extends App {
  def lRep[A] (n : Int, list : LazyList[A]) : LazyList[A] = {
    def iter (k : Int, list: LazyList[A]) : LazyList[A] = {
        list match
            case LazyList() => LazyList()
            case head #::tail => if k == 0 then iter(n, tail)
                                 else head #:: iter(k-1, list)
    }
    iter (n, list)
  }

  val test = lRep(3, LazyList(1,2,3,4,5) )
  println(test.force.toString())

  def fib() = {
    def iter (a : Int, b: Int) : LazyList[Int]= {
        a #:: iter (b, a+b)
    }
    iter(0,1)
  }

  println ( fib().take(8).force.toString())

  def lBreadth[A](tree: lBT[A]): LazyList[A] = {

  def iter(queue: LazyList[lBT[A]]): LazyList[A] =
    queue match
      case LazyList() => LazyList()
      case LEmpty #:: tail => iter(tail)
      case LNode(elem, left, right) #:: tail =>
        elem #:: iter(tail #::: LazyList(left(), right()))

  iter(LazyList(tree))
}


  val tree = LNode (1,
   () => LNode (2, () => LEmpty, () => LEmpty),
   () => LNode(3, () => LEmpty, () => LEmpty))

   print( lBreadth(tree).take(10).force)

   def lTree (n : Int) : lBT[Int] = {
        LNode (n,
        () => lTree(2*n),
        () => lTree(2*n + 1)
        )
   }

}

