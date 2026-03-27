import scala.annotation.tailrec
object zadanie extends App{

def length [A](list : List[A]) : Int = {
  @tailrec
  def iter [A] (list : List[A], count : Int) : Int ={
  list match
    case head :: tail => iter(tail, count+1)
    case Nil => count
  }
  iter(list, 0)
}
  println(List(1,2,3,4).length)
  println(List().length)
  println(List( List(),List() ).length)
  println(List( (),(),(),() ).length)
}
