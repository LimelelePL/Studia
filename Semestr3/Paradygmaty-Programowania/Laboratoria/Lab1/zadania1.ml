(*zadanie 1*)
let third (a,b,c) = c;;
let test11 = third(1,2,"j");;
(*let test12= third((1,4));;*)
let test13 = third(([], [], []));;
let test14 = third (true, 4.2, "ala");;

(* zadanie 3 *)

let rec sum list =
  if list =[] then 0.0
 else List.hd list +. sum(List.tl list);;

 let test31 = sum ([1.0;2.0;3.0;4.6;5.4]);;
 
 (*let test33 = sum(["a"; "b"]);; *)
 let test34 = sum [-1.5; 0.5; 1.0];;

 (*zadanie 4*)

 let rec lessThanNum (list, num) = 
  if list = [] then true
  else if List.hd list >= num then false
  else lessThanNum(List.tl list, num);;

  let test41 = lessThanNum([1;2;3;4;5], 6);;
  let test42 = lessThanNum( [], 0 );;
  let test43 = lessThanNum( [1;1;1;1;1], 1);;
  let test44 = lessThanNum( [3;4;5;3], 5);;
  let test45 = lessThanNum( [3;4;5;3], 4);;
  let test46 = lessThanNum([-3; -2; -1], 0);;

