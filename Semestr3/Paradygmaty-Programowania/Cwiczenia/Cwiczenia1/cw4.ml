let rec sqrList list = 
  if list = [] then [] 
  else (List.hd list * List.hd list) :: sqrList (List.tl list);;
let s = sqrList([2;3;4]);;