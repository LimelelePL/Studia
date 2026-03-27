

let rec divideList list = 
    match  list with
    | head :: tail ->
       let (even, odd) = divideList tail in
           (match head mod 2 with 
            | 0 -> (head :: even, odd)
            | _ -> (even, head :: odd))
    | [] -> ([],[]) ;;


let print_list printer lst =
  let rec aux l =
    match l with
    | [] -> ()
    | [x] -> printer x 
    | h :: t -> printer h; print_string "; "; aux t
  in
  print_string "["; 
  aux lst;
  print_endline "]";;
  
  (*zadanie 1*)
let rec reverse list =
  let rec iter (list, accum) =
    match list with
    | head :: tail -> iter (tail, head :: accum)
    | [] -> accum
    in iter (list, []) ;;

let rec divideListTail list =
  let rec helper (xs, odd, even) =
    match xs with
    | head :: tail ->
       if head mod 2 = 0 then helper (tail,  odd, head :: even)
       else helper (tail, head :: odd,  even)
    | [] -> (reverse even, reverse odd)
       in helper (list, [], []) ;;

let divide1 = divideListTail [1;2;3;4;5;6];;
let divide2 = divideListTail [];;
let divide3 = divideListTail [1;1;1;1;1;1;1;1;1];;
let divide4 = divideListTail [2;2;2;2;2;2;2;2;2];;

(*zadanie 3*)
let connect (list1, list2) = 
  let rec iter (list1, list2 ,switch, result) =
      match (list1, list2, switch) with
        | (h1::t1, h2::t2, true) -> iter(t1, h2::t2, false, h1::result)
        | (h1::t1, h2::t2, false) -> iter(h1::t1, t2, true, h2::result)
        | ([], h2::t2, _) -> iter([], t2, false, h2::result)
        | (h1::t1, [], _) -> iter(t1, [], false, h1::result) 
        | (_,_,_) -> reverse result
  in iter (list1, list2, true, []) ;;

  let connected1 = connect (['a';'b';'c'], ['A';'B';'C']);;
  let connected4 = connect ([],[]);;
  let connected2 = connect ([],[1;2]);;
  let connected3 = connect(['a';'b'],['A';'B';'C';'D']);;
  print_list print_char connected1;;
  print_list print_string connected4;;
  print_list print_int connected2;;
  print_list print_char connected3;;
  


