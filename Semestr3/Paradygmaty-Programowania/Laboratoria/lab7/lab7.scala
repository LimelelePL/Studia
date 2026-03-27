object lab7 extends App {
  
  def ldzialanie[A] (xs1: LazyList[A], xs2: LazyList[A], func : (A,A) => A) : LazyList[A] = {
    (xs1, xs2) match
      case (h1 #:: t1, h2 #:: t2) => func (h1, h2) #:: ldzialanie (t1, t2, func)
      case (LazyList(), LazyList()) => LazyList()
      case (LazyList(), h2 #:: t2) => h2 #:: ldzialanie (LazyList(), t2, func)
      case (h1 #:: t1, LazyList()) => h1 #:: ldzialanie (t1, LazyList(), func)
  }

  println("test: ldzialanie(LazyList(1,2,3,4), LazyList(1,2,3), _ + _) ")
  val test1 = ldzialanie(LazyList(1,2,3,4), LazyList(1,2,3), _ + _);
  println(test1.toList.toString());
  println("test2: ldzialanie(LazyList(a,b,c), LazyList(A,B,C), _ + _) ")
  val test2 = ldzialanie(LazyList("a", "b", "c"), LazyList("A", "B", "C"), _ + _ )
  println(test2.toList.toString())
  println("test3: ldzialanie(LazyList(1,2,3), LazyList(), (a: Int, b: Int) => a - b) ")
  val test3 = ldzialanie(LazyList(1,2,3), LazyList(), (a: Int, b: Int) => a - b)
  println(test3.toList.toString)
  println("test4: ldzialanie(LazyList(), LazyList(), (a: Int, b: Int) => a * b) ")
  val test4 = ldzialanie(LazyList(), LazyList(), (a:Int, b:Int) => a * b)
  println(test4.toList.toString)
  println("test5:val test5 = ldzialanie(LazyList.from(1), LazyList.from(1), (a:Int, b:Int) => a+b+1)")
  val test5 = ldzialanie(LazyList.from(1), LazyList.from(1), (a:Int, b:Int) => a/b)
  println(test5.take(10).toList.toString())

}
