import scala.annotation.tailrec
import scala.compiletime.ops.double
object zadania2 extends App {

/* Zadanie 1

Głębkość stosu podczas wywołania funkcji rekurencyjnej zależy od tego
ile razy funkcja wywołuje samą siebie, zanim osiągnie warunek bazowy (warunek zakończenia rekursji).
Niektóre języki takie jak OCaml i Scala są w stanie zoptymalizować niektóre typy rekurencji - takie jak
na przykład rekurencja ogonowa. 

// OCaml

OCaml jest językiem kompilowanym do kodu maszynowego:
- kompilator kontroluje cały proces generowania kodu,
- ma pełny dostęp do struktury wywołań funkcji oraz do instrukcji typu jump,
- dlatego potrafi optymalizować zarówno rekurencję ogonową,
  jak i rekurencję wzajemną.

Kod:
let rec evenR n =
  if n = 0 then true
  else oddR (n - 1)
and oddR n =
  if n = 0 then false
  else evenR (n - 1);;

Kompilator OCaml rozpoznaje wywołania w pozycji ogonowej (na końcu funkcji)
i zastępuje je instrukcją jmp (skok bez odkładania niczego na stos) zamiast call 
(który odkłada na stos adres powrotu i przechodzi do funkcji f).
Dzięki temu nie powstaje nowa ramka stosu — argumenty są nadpisywane,
a program działa jak pętla iteracyjna.

Kompilator OCamla wie, że każda z tych funkcji kończy się
na jednym wywołaniu innej funkcji i nie ma żadnych operacji po tym wywołaniu.
Dlatego nie tworzy nowej ramki stosu, tylko nadpisuje bieżącą ramkę nowymi danymi.

=> w praktyce:
   -> evenR(3)
   -> oddR(2)  (nadpisuje ramkę)
   -> evenR(1) (nadpisuje ramkę)
   -> oddR(0)  (nadpisuje ramkę) -> zwraca false -> koniec

Głębokość stosu w OCaml = 1 (stała),
ponieważ kompilator wykorzystuje optymalizację rekurencji ogonowej
(tzw. tail call optimization, TCO).


// SCALA

Głębokość stosu zależy od liczby wywołań rekurencyjnych oraz od tego,
czy kompilator musi pamiętać poprzednie wywołania, aby uzyskać poprawny wynik.

def evenR(n: Int): Boolean =
  if n == 0 then true else oddR(n - 1)

def oddR(n: Int): Boolean =
  if n == 0 then false else evenR(n - 1)

Prześledźmy działanie funkcji evenR(3) w Scali i głębokość stosu:

    -> evenR(3)   -> stos 1 false
       n != 0
    -> oddR(2)    -> stos 2 false
       n != 0 
    -> evenR(1)   -> stos 3 false
       n != 0     
    -> oddR(0)    -> stos 4  false
       n == 0  

      

Scala działa na maszynie JVM, a kod jest tłumaczony do kodu bajtowego Javy.
Maszyna JVM nie ma instrukcji typu „jump” pomiędzy metodami, więc nie może
zastąpić rekurencyjnego wywołania zwykłym skokiem (jak w językach natywnych).

W JVM każde wywołanie funkcji (metody) jest realizowane przez instrukcje 
invokevirtual, invokestatic lub invokespecial, które zawsze tworzą nową ramkę stosu
z lokalnymi zmiennymi, argumentami i adresem powrotu.
Nie istnieje możliwość wykonania „surowego” skoku (jmp) do innej metody — 
model maszyny wirtualnej Javy tego zabrania, aby zachować bezpieczeństwo
i możliwość debugowania kodu. Dlatego rekurencja wzajemna w Scali
zawsze powoduje przyrost stosu.

Aby optymalizacja mogła zajść, funkcja musi wywoływać samą siebie
i posiadać adnotację @tailrec.

Scala nie optymalizuje rekurencji wzajemnej do zwykłej rekurencji ogonowej,
mimo że obie funkcje (evenR i oddR) mają postać ogonową.
Dlatego stos osiąga głębokość 4 przy evenR(3), a przy większych n może dojść
do błędu StackOverflowError.
*/


  //zad2
  def normalFibonacci(n: Int) : Int = {
    if n==0 || n==1 then n
    else normalFibonacci(n-1) + normalFibonacci(n-2)
  }


  def tailFibonnaci(n:Int) : Int = {
    @annotation.tailrec
    def iter(n:Int, a:Int, b:Int) : Int = {
        if n == 0 then a
        else if n==1 then b
        else iter(n-1, b, a+b)
    }
    iter (n, 0, 1)
  }

  val t = tailFibonnaci(6);
  println(t)
  //zad 3

  def root3(a:Double):Double = {

    val ep : Double = 1.0e-15
    val x0 = if math.abs(a) >1 then a/3 else a
    def accuracy (xi : Double) = Math.abs(xi * xi * xi - a) <= ep * Math.abs(a)
    def next (xi : Double ) = xi + (a/(xi*xi) - xi )/3.0

    @annotation.tailrec
    def iter(result : Double):Double ={ 
        if accuracy(result) then result
        else iter(next(result))
    }
    iter(x0)
  }

    val sqr = root3(3.0)
    println(sqr)



val root3SF: Double => Double = (a: Double) => root3(a)
  
 val root3F: Double => Double = (a: Double) => { 
   val ep : Double = 1.0e-15
    val x0 : Double = if math.abs(a)>1 then a/3 else a
    val accuracy: Double => Boolean = (xi : Double) => Math.abs(xi * xi * xi - a) <= ep * Math.abs(a)
    val res: Double => Double = (xi : Double ) => xi + (a/(xi*xi) - xi )/3.0

    @annotation.tailrec
    def iter(result : Double):Double ={ 
        if accuracy(result) then result
        else iter(res(result))
    }
    iter(x0)
    }

//zad 4

val List(_, _, a, _, _) = List(-2, -1, 0, 2, 2)

val List(-2, _, b, 2, 2) = List(-2, -1, 0, 2, 2)

val _ :: _ :: c :: _ :: _ :: Nil = List(-2, -1, 0, 2, 2)

val List(_, d) = List((1,2), (0,1))

val List((1,2), (e, _)) = List((1,2), (0,1))


//zad 5
def initSegment[A](xs: List[A], ys: List[A]): Boolean = {
    (xs,ys) match {
     case (Nil, _) => true
     case (_, Nil) => false
     case (h1::t1, h2::t2) => if h1==h2 then initSegment(t1,t2) else false
    } 
}

val l = initSegment(List(1,2,3,4), List(1,2))

//zad 6
def replaceNth[A](xs: List[A], n: Int, x: A): List[A] = {
    (xs, n) match {
        case (Nil, _) => Nil
        case (h1::t1, 0) => x::t1
        case (h1::t1, _) => h1::replaceNth(t1, n-1, x)
    }
}

def replaceNthTail[A](xs: List[A], n: Int, x: A): List[A] = {
    def iter(xs:List[A], result: List[A], n:Int ) : List[A] =
    xs match {
        case (Nil) => result.reverse
        case (h1::t1) => if n!=0 then iter(t1, h1::result , n-1) else iter(t1, x :: result, n-1)
    }
    iter(xs, Nil, n)
}

val replaced = replaceNthTail(List(1,2,3,4), 2, 10);
print(replaced.toString())

/* wspoldzieli ogon ta lista np:
    replaceNth(List(1,2,3,4,5), 2, 10)
    1 :: ReplaceNth (List(2,3,4,5), 1 , 10)
    1 :: (2 :: ReplaceNth (List(3,4,5), 0 , 10))
    1 :: (2 :: (10 :: [3,4,5])) -> ten sam ogon
    
    w pameci
    1 -> 2 -> 10  (nowa lista zawiera nową część 1 -> 2 -> 10 ale stary ogon 3->4->5 wspoldzieli ze stara lista)
                \
        1 -> 2 -> 3 -> 4 -> 5 (stara lista) 

 */


}