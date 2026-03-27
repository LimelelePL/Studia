import scala.annotation.tailrec
object zadania extends App
{
    def reverse [A] (list: List[A]) : List[A] = {
        @tailrec
        def iter (list: List[A], accum: List[A]) : List[A] = {
            list match
                case head :: tail => iter(tail, head :: accum)
                case Nil => accum
        }   
        iter (list, Nil)
    }

    def addVectors (list1 : List[Double], list2: List[Double]) : List[Double] = {
        val neutralValue = 0
        @tailrec
        def iter (list1: List[Double], list2: List[Double], result: List[Double]) : List[Double] = {
            (list1, list2) match
                case (h1::t1, h2::t2) => iter (t1, t2, (h1+h2) :: result)
                case (Nil, h2::t2) => iter (list1, t2, (neutralValue + h2):: result)
                case (h1::t1, Nil) => iter (t1, list2, (neutralValue + h1):: result)
                case (Nil,Nil) => result.reverse
            }
        iter(list1, list2, Nil)
    }

println(addVectors(List(1,2,3), List(4,5,6,7,8)))  
println(addVectors(List(1.3,2.9,3,4.4,5,6), List(1,2,3))) 
println(addVectors(Nil, List(1,2,3)))               
println(addVectors(List(1,2,3), Nil))             
println(addVectors(Nil, Nil))   

} 
