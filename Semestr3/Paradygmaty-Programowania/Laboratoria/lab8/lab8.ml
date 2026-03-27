type 'a llist = LNil | LCons of 'a * (unit -> 'a llist)

let rec ltake (n, lxs) =
match (n, lxs) with
(0, _) -> []
| (_, LNil) -> []
| (n, LCons(x,xf)) -> x::ltake(n-1, xf())
;;
let printIntList list =
  let r = ref list in
  while not (List.is_empty !r) do
    print_int (List.hd !r);
    print_string " ";
    r := List.tl !r
  done;
  print_newline ()
;;

  let lazyFibN n = 
    if n<0 then failwith "n musi byc wieksze od 0" else
    let rec helper n a b = 
      if n = 0 then LNil
      else if  a < 0 || b < 0 then failwith "overflow"
      else LCons (a, fun () -> helper (n-1) (b) (b+a))
    in helper (n+1) 0 1;;

  printIntList (ltake (1, lazyFibN 0));;
  printIntList (ltake (6, lazyFibN 5));;
  printIntList (ltake (10, lazyFibN (max_int)));;
  printIntList (ltake (10, lazyFibN (-1)));;

  





  


   



    


