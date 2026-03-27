object cw5 extends App { 

def isPalindrome [A] (list : List[A]) : Boolean = {
  list == list.reverse
}
val isPalindrome: [A] => List[A] => Boolean = [A] => (list: List[A]) => 
    list == list.reverse

def listLength [A] (list: List[A] ) : Int = 
  if list == Nil then 0
  else 1 + listLength(list.tail)


val l = listLength(List(1,2,3))

}
