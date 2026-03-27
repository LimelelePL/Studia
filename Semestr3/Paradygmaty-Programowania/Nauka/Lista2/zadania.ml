


let repetition list =
  let rec iter (lst, times, accum, result) =
    match (lst, accum) with 
      |([], _) -> List.rev result
      |(head::tail, 0) -> iter(tail, times+1 ,times+1, result)
      |(head::tail, _) -> iter(lst, times, accum-1, head::result) 
    in
      iter(list, 1,1, []);;
      
let rep = repetition([1;2;3;4]);;