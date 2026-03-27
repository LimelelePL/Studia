
let reverse list = 
  let rec iter (list, accum) = 
    match list with 
      | head :: tail -> iter (tail, head :: accum)
      | []  -> accum
  in iter (list, []);;

let divideList list = 
  let rec iter (list, idx, p1, p2, p3) = 
    match list with 
   | head :: tail ->
           (
            match idx mod 3 with
              | 0 -> iter (tail, idx+1, head :: p1, p2, p3)
              | 1 -> iter (tail, idx+1, p1, head::p2, p3)
              | _ -> iter (tail, idx+1, p1, p2, head :: p3)
           )
   | [] -> (reverse p1 ,reverse p2 , reverse p3)
   in iter (list, 0, [], [], []);;


let t1 = divideList [5;4;3;2];;
let t2 = divideList [1;2;3;4;5;6;7;8;9];;
let t3 = divideList [];;
let t4 = divideList [10];;
let t5 = divideList [1;2;3;4;5;6;7];;
