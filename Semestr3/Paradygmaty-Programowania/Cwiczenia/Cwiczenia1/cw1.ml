
let rec flatten list = 
  if list = [] then []
  else List.hd list @ flatten(List.tl list);;
  let flattened = flatten [[3; 4]; [3; 6]];;
    let flattened2 = flatten [[]; []];;
