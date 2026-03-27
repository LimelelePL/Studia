object zadania1 extends App{
  //zadanie 2
  def genList(num1: Int, num2:Int): List[Int] = 
    if num1 == num2 then List(num1)
    else if num1 < num2 then num1::genList(num1+1, num2)
    else num2::genList(num2+1, num1)
  
  val t21 = genList(2,9)
   println(t21.toString())
  val t22 = genList(0,0)
   println(t22.toString())
  val t23 = genList(9, 1)
   println(t23.toString())
  val t24 = genList(-2,2) 
   println(t24.toString())
}