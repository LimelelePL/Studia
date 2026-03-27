object list3 extends App {
  
  /* 
  Zad. 1. [3+2p] Wykorzystując rekurencję ogonową i mechanizm dopasowania wzorca
napisać w Scala funkcję znajdującą minimalną i maksymalną wartość w każdej liście
umieszczonej w liście list. Wynik umieścić w liście par składających się z minimalnych i
maksymalnych wartości. Napisać następnie równoważną funkcję z jednokrotnym
wykorzystaniem funkcjonałów map i foldLeft.

Zad. 2. [3p] Zakładając, że lista modeluje wektor w przestrzeni o dowolnym wymiarze
napisać w OCaml wykorzystujący rekurencję ogonową operator (+) dodający dwa dowolne
wektory. W przypadku gdy wymiary wektorów się różnią, obliczenia wykonać dla przestrzeni
o wyższym wymiarze (wektor pochodzący z przestrzeni o niższym wymiarze potraktować
tak jakby pochodził z przestrzeni o wyższym wymiarze tzn. posiadał dodatkowe zerowe
współrzędne).

Zad. 3. [2p] Wyznaczyć wartość g’(f’(x)) dla zadanego x. Funkcje f i g są dowolnymi
wcześniej zdefiniowanymi funkcjami wykorzystującymi wielomian i funkcje
trygonometryczne lub logarytm. Uwzględnić fakt, że wartość ilorazu różnicowego jest
przybliżeniem wartości pochodnej funkcji. Iloraz różnicowy należy specjalizować dla
dx=0.0000001. Zadanie wykonać w Scala.
 */

def findMaxInAllLists(list: List[ List[Int] ]) : List[(Int, Int)] = {

def innerIter(list : List[Int]  , max : Int, min:Int) : (Int,Int) = {
    list match
        case h::t => if h > max then innerIter(t, h, min)
                    else if h < min then innerIter(t, max, h) 
                    else innerIter(t, max, min)
        case Nil => (max, min)
    } 

def iter(list: List[ List[Int]], accum: List[(Int, Int)]) : List[(Int, Int)] = {
    list match
        case head::tail if head.isEmpty => iter(tail, (0,0) :: accum)
        case head :: tail => iter(tail, innerIter(head, head.head, head.head) :: accum)
        case Nil => accum.reverse
    } 
    iter(list, Nil)
}

val inputList: List[List[Int]] = List(
  List(5, 1, 9, 3, 7),
  List(42),
  List(10, 20, 5, 15),
  List(100, 50, 200, 10)
)

def minMaxAll(data: List[List[Int]]): List[(Int, Int)] =
  data.map(xs =>
    xs.tail.foldLeft((xs.head, xs.head)) {
      case ((min, max), x) => (math.min(min, x), math.max(max, x))
    }
  )

def addVector(v1: List[Int], v2: List[Int]) : List[Int] = {
  v1.zip(v2).map { 
    case (elemA, elemB) => elemA + elemB
    }
}
println(addVector(List(3,3,3), List(1,2,3)).toString())

def f(x: Double) = x*x + math.sin(x)
def g(x: Double) = math.log(x + 5)
def derivative (f : Double => Double, x : Double) : Double = {
   (f(x + 0.0000001) - f(x)) / 0.0000001
}

val res = derivative( f, g(2.0) )
println(res)

val result = findMaxInAllLists(inputList)
println(result.toString());

}
