type graph = (int*int list) list


let reachableCount (graph:graph) start = 
  let rec get graph elem = 
    match graph with 
      | head :: tail when (fst head) = elem -> ((fst head), (snd head))
      | head :: tail -> get tail elem
      | _ -> failwith ("nie zdefiniowano w grafie wierzchołka: " ^ string_of_int elem)
  in
    let rec isVisited elem list = 
    match list with
    | head :: tail when head = elem -> true
    | head :: tail -> isVisited elem tail
    | [] -> false
  in
    let rec iter accum queue visited = 
      match queue with 
        | [] -> accum
        | top :: bottom -> 
          let (elem, neighbours) = get graph top 
        in
          if isVisited elem visited then iter accum bottom visited 
          else iter (accum+1) (bottom @ neighbours) (elem :: visited)
        in iter (0) [start] [];;

      print_string("======= ZADANIE 1 =======");;
      print_newline ();;

let g1: graph = [
  (1, [2; 3]);
  (2, [4]);
  (3, [4; 5]);
  (4, []);
  (5, [4]);
];;

print_int (reachableCount g1 1);;
print_newline ();;

let g2: graph = [
  (1, []);
  (2, []);
  (3, []);
];;

print_int (reachableCount g2 1);;
print_newline ();;

let g3: graph = [];;


(try
   print_int (reachableCount g3 1)
 with Failure msg ->
   print_string ("Exception: " ^ msg)
);;

print_newline ();;

let g4: graph = [
  (1, [2]);
  (2, [1]);
];;

print_int (reachableCount g4 1);;
print_newline ();;

 print_newline ();;
 print_string("======= ZADANIE 2 =======");;
 print_newline ();;


type 'a tree =
  Empty
| Node of 'a * 'a tree * 'a tree

let treeStats (tree : int tree) = 
  let rec iter stack maxDepth numOfNodes = 
    match stack with 
      | [] -> (numOfNodes, maxDepth)
      | (node, depth) :: tail ->
        match node with 
          | Empty -> 
              iter (tail)(maxDepth)(numOfNodes)
          | Node(elem, left, right) ->
              iter ((left, (depth+1)) :: (right, (depth+1)) :: tail) (max maxDepth depth) (numOfNodes + 1) 
          in
          match tree with
          | Empty -> (0, 0)
          | _ -> iter [(tree, 1)] 0 0
        ;;

      let printTreeStats tree =
        let (num, depth) = treeStats tree in
        Printf.printf "Głębokość: %d, liczba wezlow: %d\n" depth num;;

      let tree = Node(1,Node(2,Empty,Empty),Empty);;
      (*
            1
          2
      *)
      printTreeStats tree;;
      let tree1 = Node(1,Node(2,Node (3, Node (4,Node(5,Empty,Empty),Node(6,Empty,Empty)),Empty),Node(0,Empty,Empty)),Empty);;
      (*
            1
          2
        3   0
      4
    5   6
      *)
      printTreeStats tree1;;
      let tree2 = Node(1,Empty, Empty);;
      printTreeStats tree2;;
      let tree3 = Empty;;
      printTreeStats tree3;;

      

         