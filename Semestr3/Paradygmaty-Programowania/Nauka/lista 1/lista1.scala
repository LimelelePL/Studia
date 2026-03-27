object lista1 extends App {
  
  /* Napisać funkcję fiddle4 zmieniającą elementy podanej krotki czteroelementowej w
następujący sposób: (1.3, 2.0, 3.1, 4.2) -> (4.2, 1.3, 3.1 - 2.0). (OCaml i Scala) (10pkt.) */

def fiddle4[A](krotka: (A, A, A, A)): (A, A, A, A) = {
  val (x, y, z, w) = krotka
  (w, y, z, x)
}


/* Napisać funkcję hits przyjmującą dwie listy i zliczającą na ilu pozycjach są one równe. (OCaml
i Scala) (10pkt.) */

def hits [A] (l1 : List[A], l2 : List[A]) : Int = {
    if l1.isEmpty || l2.isEmpty then 0
    else if l1.head == l2.head then 1 + hits(l1.tail , l2.tail)
    else hits(l1.tail, l2.tail)
    }

println(hits ( List(1,2,3), List(1,2,4) ) )

/*3) Napisać funkcję insert przyjmującą listę, nowy element oraz pozycję, na którą ma on być
wstawiony i zwracającą nową listę zawierającą wstawiany element. Jeśli pozycja jest poza
zakresem, element należy wstawić na odpowiednim końcu listy. (OCaml i Scala) (10pkt.) */

def insert [A] (l : List[A], elem : A, pos: Int) : List[A] = {
  if l.isEmpty then elem :: l
  else if pos>0 then l.head :: insert (l.tail, elem, pos-1)
  else elem :: l //pos dochodzi do zera i mozemy skladac liste na nowo 
}

val list = insert(List(1,2,3,4,5), 10, 3)
print (list.toString())

/*
4) Napisać funkcję militaryMinutes przyjmującą trójkę wartości: dwie liczby reprezentujące
godzinę i minuty w systemie 12-o godzinnym oraz łańcuch znaków zawierający porę dnia –
„AM” / „PM”, i zwracającą napis zawierający tę godzinę w systemie 24-o godzinnym postaci:
„HH : MM”. W razie błędu rzucić wyjątek z odpowiednim komunikatem tekstowym. (OCaml i
Scala) (20pkt.)
*/

def militaryMinutes (godzina : Int, minuta: Int, pora : String ): String = {

  if godzina > 12 || godzina <0 then throw new IllegalArgumentException("Nieprawidlowa godzina")
  
  val godzinaPM ={
     if(godzina + 12) >= 24 then godzina - 12
     else godzina + 12
     }
  
  if (pora == "AM") then s" $godzina : $minuta" 
  else if (pora == "PM") then s" $godzinaPM : $minuta"
  else throw new IllegalArgumentException("nieprawidlowa godzina lub pora")
} 

val t = militaryMinutes(12, 30, "PM")
print(t)

/* 
Zadanie 1 — funkcja zip

Treść:

Napisz rekurencyjną funkcję zip, która przyjmuje dwie listy
i zwraca listę par (krotek) utworzonych z odpowiadających sobie elementów obu list.
Jeśli jedna z list jest krótsza, wynikowa lista powinna mieć długość tej krótszej.

Wskazówka: użyj dopasowania do wzorca (match) i operatora :: do rozbicia list.
*/

/* Zadanie 2 — funkcja unzip

Treść:
Napisz rekurencyjną funkcję unzip, która przyjmuje listę par
i zwraca parę list: pierwsza lista zawiera wszystkie pierwsze elementy par,
a druga — wszystkie drugie elementy.
Funkcja ma być odwrotnością zip.
Wskazówka: wykorzystaj dopasowanie do wzorca (h1, h2) :: t
oraz wywołanie rekurencyjne dla reszty listy t. */

/* Napisać w Scala funkcję sprawdzającą czy elementy danej listy liczb
całkowitych są posortowane nierosnąco. */

def areSorted (l: List[Int]): Boolean ={
   l match {
    case Nil => true
    case List(c) => true
    case a :: b => a>b.head && areSorted(b.tail)
    }
  }


  val sorted = areSorted(List(5,9,3,2,1))
  println( sorted )
}



