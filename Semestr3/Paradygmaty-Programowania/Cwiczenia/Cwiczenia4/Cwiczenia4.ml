(*zadanie 1*)
let f1 x y z = x y z;;

(* funkcja x przyjmuje argument y typu 'a a nastepnie zwraca funkcje przyjmującą argument z typu 'b
cała funkcja x y z zwraca 'c czyli x: a'->b'->c'

funkcja f1 jest zatem typu (a'->b'->c') -> a'->b'->c'
*)

let f2 x y = function z -> x::y;;

(*
x::y oznacza łączenie elemntu x z listą y czyli x: a', y 'a list
typ x::y : a'list

ponieważ wynik funkcji f2 jest funkcją anonimową i jej argument z nie jest uzywany w ciele funkcji
to dajmy mu typ 'b

funkcja f2 przyjmuje argumenty x i y czyli f2: a' -> a'list -> (b' -> a'list)
*)

(*zadanie 2*)
let f y = failwith "Funkcja f: 'a -> 'b nie ma sensownej implementacji";;
let rec f x = f x;;



(*zadanie 3
 Dla drzew binarnych, zdefiniowanych na wykładzie, napisz funkcję breadthBT : 'a bt -> 'a list
 obchodzącą drzewo wszerz i zwracającą zawartość wszystkich węzłów drzewa w postaci listy.
*)

type 'a tree =
 Empty | Node of 'a*'a tree* 'a tree;;
 let tt =
 Node(1,Node(2,Node(4,Empty,Empty),Empty),  
 Node(3,
 Node(5,Empty, Node(6,Empty,Empty)),Empty));; 

 let breadthBT tree = 
  let rec helper queue acc = 
    match queue with
    | [] -> List.rev acc;
    | Empty :: rest -> helper rest acc
    | Node(elem, left, right) :: rest -> helper (rest @ [left ; right]) (elem::acc)
  in helper [tree] [];;

    let test = breadthBT tt;;

    let internalPath tree =
      let rec helper tree depth = 
        match tree with
        | Empty -> 0
        | Node(_, left, right) -> depth + helper left (depth + 1) + helper right (depth + 1)
      in helper tree 0;;
    
    let externalPath tree = 
      let rec helper tree depth =
        match tree with
        | Empty -> depth
        | Node(_, left, right) ->helper left (depth + 1) + helper right (depth + 1)
      in helper tree 0;;


      print_int (internalPath tt);;

      type 'a graph = Graph of ('a -> 'a list);;
    let dfs (Graph graph) startNode = 
      let rec search visited stack= 
        match stack with 
          | [] -> []
          | top :: bottom ->
             if List.mem top visited then search visited bottom
             else top :: search (top::visited) (graph top @ bottom)
          in search [] [startNode];;
          
      let g = Graph (function
          | 0 -> [3]
          | 1 -> [0;2;4]
          | 2 -> [1]
          | 3 -> []
          | 4 -> [0;2]
          | n -> failwith ("Graph g: node "^string_of_int n^" doesn't exist")
          );;   

          let dfsTest = dfs g 4;;

    








 