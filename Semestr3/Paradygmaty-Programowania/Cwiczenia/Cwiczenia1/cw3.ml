let rec replicate (elem, n) = 
  if n == 0 then []
  else elem :: replicate(elem, n-1);;

let replicated = replicate (10, 3);;