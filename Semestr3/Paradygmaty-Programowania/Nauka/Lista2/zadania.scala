object zadania extends App {
  /* 1. [OCAML] Stwórz dwuargumentową funkcję, która w czasie liniowym sprawdzi czy pierwszy
string jest częścią drugiego np.
a. f(‘raz’, ‘obraz’) -> true
b. f(‘obraz’, ‘raz’) -> false
Wykorzystaj mechanizm dopasowania do wzorca. – 2pkt. (1+1)
2. [SCALA] Napisz funkcję dwuargumentową — komparator(def less(str1: String, str2: String):
Boolean), który porównuje dwa napisy. Funkcja powinna zwrócić true wtedy i tylko wtedy,
gdy pierwszy napis w słowniku wystąpiłby wcześniej. W przeciwnym razie funkcja ma
zwrócić false. Np. wartość false zwrócą wywołania less("my", "my") lub
less("mysz", "my"), wartość true zwrócą wywołania less("my",
"mysz"), less("myk", "mysz"). Użyj tej funkcji jako komparator do
funkcji List.sortWith zademonstruj działanie sortując listę napisów. Wykorzystaj
mechanizm dopasowania do wzorca i rekursję ogonową. Czym jest rekursja ogonowa? – 4 pkt.
(2+2)
3. [OCAML] Stwórz dwuargumentową funkcję drop, która wyrzuci z listy co n-ty element. Funkcja
powinna przyjmować n-ty element i listę np. :
drop(3, [‘a’, ‘b’, ‘c’, ‘d’, ‘e’, ‘f’, ’g’, ‘h’]) -> [‘a’, ‘b’, ‘d’, ‘e’, ‘g’ ‘h’] – 3 pkt. (1+2)
4. [SCALA] Stwórz funkcję, która przeanalizuje listę i stworzy listę krotek reprezentujących ilość
wystąpień elementów w liście wejściowej np.
analyse([‘a’, ‘b’, ‘c’, ‘c’, ‘a’]) -> [(‘a’, 2), (‘b’,1), (‘c’, 2)] – 6 pkt. (3+3)


Zad. 1. [4p] Napisać w OCaml funkcję o typie 'a list * int -> 'a list dokonującą podziału
zadanej listy na dwie podlisty: listę elementów przed (włącznie) i listę elementów po
elemencie o zadanej pozycji, zwracającą listę powstałą z połączenia podlist w odwróconej
kolejności.
Zad. 2. [4+2p] Wykorzystując mechanizm dopasowania wzorca napisać w OCaml funkcję
typu 'a list -> 'a list (jedną!) stosującą rekurencję ogonową, która przekształca wejściową
listę do postaci, w której każdy element listy jest powtórzony liczbę razy równą pozycji
elementu w liście wejściowej. Zadanie wykonać następnie w Scala. */

// 
def partition[A] (list : List[A], index:Int) : List[A] ={
    def iter[A] (list: List[A], accum: List[A], index:Int) : List[A] =
    (list, index) match
        case (Nil,_)=> list
        case (head :: tail, 0) => list ::: accum.reverse
        case (head :: tail, _) => iter(tail, head :: accum, index-1 )
    
    iter(list, Nil, index)
}
  
  val partitioned = partition(List(1,2,3,4,5,6), 3)
  print(partitioned.toString())

}
