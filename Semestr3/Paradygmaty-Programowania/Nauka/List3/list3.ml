(*Zad. 2. [3p] Zakładając, że lista modeluje wektor w przestrzeni o dowolnym wymiarze
napisać w OCaml wykorzystujący rekurencję ogonową operator (+) dodający dwa dowolne
wektory. W przypadku gdy wymiary wektorów się różnią, obliczenia wykonać dla przestrzeni
o wyższym wymiarze (wektor pochodzący z przestrzeni o niższym wymiarze potraktować
tak jakby pochodził z przestrzeni o wyższym wymiarze tzn. posiadał dodatkowe zerowe
współrzędne).*)

let (+) (a,b) = 
  let rec iter(a, b, accum) = 
    match (a,b) with
    | ( h1::t1, [] ) -> iter( t1, [], h1::accum)
    | ([], h2 :: t2) -> iter([], t2, h2::accum)
    | ( h1::t1, h2::t2 ) -> iter(t1,t2, (h1+h2) :: accum)
    | ([],[]) -> List.rev accum
  in iter(a,b, [])
;;

(* Oczekiwane: [11; 22; 33] *)
let test1 = (+) ([10; 20; 30], [1; 2; 3;5]);;
