(* Podaj (i uzasadnij!) najogólniejsze typy poniższych funkcji (samodzielnie, bez pomocy kompilatora
OCamla!) :
 a) let f1 x = x 2 2;; b) let f2 x y z = x ( y ^ z );; *)

 (*
 A) funkcja x przyjamuje argument int i zwraca funkcje ktora przyjmuje także argument int i zwraca "coś" czyli:
 x: int ->( int -> a ) = int -> int -> a
 typ: (int -> int -> a) -> a bo f1 zwraca to samo co x

 B) operator ^ łączy stringi czyli y -> string i z -> string czyli argumentem funkcji x jest string czyli:
 x: string -> a
 funckja f2 jest trójargumentowa i zwraca taki sam typ jak x
 (string -> a) -> string -> string -> a
 *)

 (*
 2. Zdefiniuj funkcje a) curry3 i b) uncurry3, przeprowadzające konwersję między zwiniętymi i rozwiniętymi
 postaciami funkcji od trzech argumentów. Podaj (i uzasadnij!) ich typy.
 Dla każdej funkcji napisz dwie wersje: z lukrem syntaktycznym i bez lukru syntaktycznego
 *)


 let curry3 f a b c = f (a,b,c);;
 let curry3 = fun f -> fun a -> fun b -> fun c -> f (a,b,c);;
 let uncurry3 f(a,b,c) = f a b c;;
 let uncurry3 = fun f -> fun(a,b,c)  -> f a b c

 (*Sprawdzian 2 na eportalu wrzucic*)
 let curry4 f a b c d = f(a,b,c,d) ;; (* lukier*)
 let curry4 = fun f-> fun a -> fun b -> fun c -> fun d -> f(a,b,c,d);; (*brak lukru*)
 let uncurry4 f(a,b,c,d) = f a b c d;; (*lukier*)
 let uncurry4 = fun f -> fun(a,b,c, d)  -> f a b c d;; (*brak lukru*)


 (*
 przekształć poniższą rekurencyjną definicję funkcji sumProd, która oblicza jednocześnie
 sumę i iloczyn listy liczb całkowitych na równoważną definicję nierekurencyjną z
 jednokrotnym użyciem funkcji bibliotecznej fold_left (Scala – foldLeft), której argumentem jest
 odpowiednia funkcja anonimowa (literał funkcyjny).
 *)

 let rec sumProd xs = 
   match xs with 
   | h::t -> let (s,p) = sumProd t in (h+s, h*p)
   | [] -> (0,1);;
let sumProd xs = List.fold_left (fun accum elem -> match accum with (a,b) -> (a+ elem, elem * b)) (0,1) xs;;

(*zadanie 4*)

let rec quicksort = function
 [] -> []
 | [x] -> [x]
 | xs -> let small = List.filter (fun y -> y < List.hd xs ) xs
 and large = List.filter (fun y -> y >= List.hd xs ) xs
 in quicksort small @ quicksort large;;

 (* W niektórych przypadkach poniższy algorytm nie działa poprawnie, ponieważ filtruje listy
 wraz z pivotem. W efekcie pivot z poprzedniego wywołania może trafić do listy `large`. 

 W poprawnym wariancie algorytmu pivot powinien być jedynie użyty do porównywania elementów
 (czyli do filtrowania), ale nie powinien znajdować się już w filtrowanej liście.

 Następnie pivot należy umieścić pomiędzy posortowaną listą `small` i posortowaną listą `large`
 w wyniku końcowym. *)
let s = quicksort [5;4;3];;

let rec quicksort' = function
 [] -> []
 | x::xs -> let small = List.filter (fun y -> y < x ) xs
 and large = List.filter (fun y -> y > x ) xs
 in quicksort' small @ (x :: quicksort' large);;

 let ss = quicksort'[6;6;9];;

 (*Ta wersja nie działa poprawnie w przypadku list zawierających powtarzające się wartości.
 Lista `large` jest tworzona przy użyciu filtra `(fun y -> y > x)`, 
 przez co elementy równe pivotowi `x` nie trafiają ani do `small`, ani do `large`
 i w efekcie zostają zgubione.*)


let insertionSort comp xs =
  let rec insert xs elem =
    match xs with
    | head :: tail ->
        if comp elem head then elem :: xs
        else head :: insert tail elem
    | [] -> [elem]
  in
  let rec sort xs sortedPart =
    match xs with
    | head :: tail -> sort tail (insert sortedPart head)
    | [] -> sortedPart
  in
  sort xs []
;;

let comp (key1, _) (key2, _) = key1 < key2;;
let stInser = insertionSort comp [(2,'C');(1,'A'); (1,'B')];;

let mergeSort comp xs =
  let rec merge comp result xs ys =
    match (xs, ys) with
    | (h1 :: t1, h2 :: t2) ->
        if comp h1 h2 || not (comp h2 h1) then
          merge comp (h1 :: result) t1 ys
        else
          merge comp (h2 :: result) xs t2
    | ([], h2 :: t2) -> List.rev result @ ys
    | (h1 :: t1, []) -> List.rev result @ xs
    | ([], []) -> List.rev result
  in
  let partition xs =
    let rec iter xs fast slow left right =
      match (fast, slow) with
      | (h1 :: a :: b, h2 :: t2) -> iter xs b t2 (h2 :: left) (h2 :: t2)
      | (h1 :: [], h2 :: t2) -> (List.rev left, h2 :: t2)
      | ([], h2 :: t2) -> (List.rev left, h2 :: t2)
      | _ -> (List.rev left, [])
    in
    iter xs xs xs [] []
  in
  let rec sort xs =
    match xs with
    | [] -> []
    | [_] -> xs
    | _ ->
        let (a, b) = partition xs in
        merge comp [] (sort a) (sort b)
  in
  sort xs
;;

let s = mergeSort (fun a b -> a<b ) [2;4;6;3;1;2;1];;
let s1 = mergeSort (fun a b -> a<b ) [2;4];;
let s2 = mergeSort (fun a b -> a<b ) [2;4;6];;
let s3 = mergeSort (fun a b -> a<b ) [2;4;6;3;1;2;1];;
let st = mergeSort comp [(2,'C');(1,'A'); (1,'B')];;
      



