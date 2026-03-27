
let duplicate list1 list2 =
  let rec iter l1 l2 acc =
    match l1, l2 with
    | [], _ | _, [] -> List.rev acc
    | x :: xs, n :: ns ->
        let rec repeat k acc =
          if k <= 0 then acc
          else repeat (k - 1) (x :: acc)
        in
        iter xs ns (repeat n acc)
  in
  iter list1 list2 []
;;

let test =duplicate [1;2;3] [];;

let add list elem comp = 
  let rec iter list accum = 
    match list with
    | [] -> List.rev (elem :: accum )
    | head :: tail -> 
      (*jezeli element wiekszy od glowy*)
      if comp elem head then iter tail (head :: accum)
      else (List.rev (elem :: accum)) @ list
    in 
    iter list [] ;; 

    let comp a b = a > b;;
    let test = add [1;5;6;8;10] 7 comp;;

