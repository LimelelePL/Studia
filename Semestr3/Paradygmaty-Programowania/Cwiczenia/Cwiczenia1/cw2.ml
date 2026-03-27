

let rec count (elem , list) =
  if list = [] then 0
  else if List.hd list = elem then 1 + count (elem, List.tl list)
  else count (elem, List.tl list);;


  let value = count (3, [2;2;4;3;3]);;
  print_int value;;