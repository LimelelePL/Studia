type 'a llist = LNil | LCons of 'a * 'a llist Lazy.t;;

  let rec lfrom k = LCons (k, lazy (lfrom (k+1)));;
let rec toLazyList = function
 [] -> LNil
 | x :: xs -> LCons(x, lazy (toLazyList xs))
;;
let rec ltake = function
 (0, _) -> []
 | (_, LNil) -> []
 | (n, LCons(x, lazy xs)) -> x :: ltake(n-1, xs)
;; 

(*
head :: tail = Lcons(a, lazy tail)
czyli np head :: iter( n-1, list) =  Lcons (head, lazy (iter(n-1, list)))
*)

let lRep n lList = 
  let rec iter k lList = 
    match lList with 
      | LNil -> LNil
      | LCons(head, lazy tail) -> 
          if k = 0 then iter n tail
          else LCons (head, lazy (iter (k-1) lList) )
        in iter n lList
      ;;

  let test = ltake (6, (lRep 2 (toLazyList["a";"b";"c";"d";"e"])));;


  let lfib = 
    let rec iter a b = 
      LCons(a, lazy (iter (b)(a+b)))
    in iter 0 1
  ;;

    let testfib = ltake (6, lfib);;

    type 'a lBT = LEmpty | LNode of 'a * (unit ->'a lBT) * (unit -> 'a lBT);;

    let iBreadth tree =
      let rec helper queue = 
        match queue with
          | [] -> LNil
          | head :: tail -> 
              match head with 
                | LEmpty -> helper tail
                | LNode (elem, left, right) ->
                    LCons (elem, lazy (helper (tail @ [left(); right()])))
                in helper [tree];;

      let t2 = LNode(1,
        (fun () -> LNode(2, (fun () -> LEmpty), (fun () -> LEmpty))),
        (fun () -> LNode(3, (fun () -> LEmpty), (fun () -> LEmpty))));;
  let t = ltake (3, iBreadth t2);;
        
    let rec lTree n =
      LNode (n,
         (fun () -> lTree (2 * n)),
         (fun () -> lTree (2 * n + 1)))
;;





              