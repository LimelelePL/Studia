
(*zadanie 1*)
let filterList (list, value) = 
  List.filter (fun sublist -> (List.fold_left (fun acc x -> acc + x) 0 sublist) = value) list;;

let t1a = filterList([[1;2;3];[2;5];[5;6]], 6);;
let t1b = filterList([[1;2];[2;5];[5;-5]], 0);;
let t1c = filterList([[1;2;3];[2;5];[5;6]], 0);;
let t1d = filterList([[];[];[]], 0);;
let t1e = filterList([[1;2;-3];[2;5];[-5;-5]], -10);;


(*zadanie 2*)
let convertToDecimal list = 
  List.fold_left (fun acc x -> 
    if x <> 0 && x <> 1 then failwith "Niepoprawna cyfra binarna!" 
    else x + 2*acc) 0 list;;

let t2a = convertToDecimal [1;1;1;0] ;;
let t2b = convertToDecimal [0;0;0;0] ;;
let t2c = convertToDecimal [1;1;1;1;1;1;1] ;;
let t2d = convertToDecimal [0;3;0;0] ;;

(*zadanie 3*)
let connect list = 
  List.map (fun x -> match x with (a,b,c,d) -> a^b^c^d ) list;;
let t3a = connect [("ala","ma","kot","a"); ("kot","nie","ma","ali")];;
let t3b = connect [("a","","b","c"); ("x","y","z","w")];;
let t3c = connect [("","a","b","c")];;
let t3d = connect [("1","2","3","4"); ("a","b","c","d")];;
let t3e = connect [];;



