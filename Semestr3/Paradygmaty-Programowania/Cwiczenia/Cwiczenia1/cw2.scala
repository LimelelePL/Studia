object cw2 extends App {

def count[A](elem: A, list: List[A]): Int = {
  if list == Nil then 0 
  else if list.head == elem then 1 + count(elem, list.tail)
  else count(elem, list.tail)
}

val c = count(3, List(3,4,5,3,2) )
print(c)
    
}