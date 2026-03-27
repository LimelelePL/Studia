
let fiddle4 (a,b,c,d) = (d,b,c,a);;

let rec hits (list1, list2) = 
  if list1 = [] || list2 = [] then 0
  else if List.hd list1 = List.hd list2 then (1+hits(List.tl list1, List.tl list2))
  else hits(List.tl list1, List.tl list2);;

let test = hits ([1;2;3], [2;2;3]);;

let rec insert (list, elem, pos) = 
  if list = [] then elem::list
  else if pos > 0 then List.hd list ::insert(List.tl list, elem, pos-1)
  else elem :: list ;;

let inserted = insert([1;2;3], 10, 1);;

let militaryMinutes (hour, minute, str) =
  if hour > 12 || hour < 0 then failwith"wrong time"
 else
    let convertHour = 
    if(hour + 12 >= 24 ) then (hour - 12)
    else (hour + 12)
  in
    if str = "PM" then string_of_int convertHour ^ ": " ^ string_of_int(minute)
    else if str = "AM" then string_of_int hour^ ": " ^ string_of_int(minute)
    else failwith("wrong str") ;;

let te = militaryMinutes(12, 30, "PM") ;;

(*[OCAML] Napisz funkcję zwracającą wszystkie liczby pierwsze z podanego przez parametr
funkcji zakresu(może być krotka o dwóch wartościach). – 3 pkt. (2+1)*)

let isPrime(a) =
if a <= 0 then false 
else if (a = 1) || (a = 2) then true
else let rec check (iter) =
      if iter = a then true
      else if a mod iter = 0 then false
      else check(iter+1)
  in check 2 ;;

let rec allPrime (a, b) =
  if a > b then []
  else if isPrime a then a :: allPrime (a + 1, b)
  else allPrime (a + 1, b);;


let v = allPrime(0,10);;
let print_int_list l =
  List.iter (fun x -> print_int x; print_string " ") l;
  print_newline ();;

print_newline;;
print_int_list v;;

  
