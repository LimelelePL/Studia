
(*
let f a b = (b a, a)

typ a to 'a
typ b to 'a->'b

typ f: 'a -> ('a -> 'b) -> 'b * 'a

let g x y z = if y z then [x] else []

typ x to 'a
typ z to 'b
typ y to 'b -> bool

typ g: 'a -> ('b -> bool) -> 'b -> 'a list
*)
let rec sumdigits num = 
    let rec numToList num accum = 
        if num = 0 then List.rev accum else numToList (num/10) ((num mod 10) :: accum)
in 
    let numAsList =  numToList num []
in
    List.fold_left (fun accum elem -> elem + accum) 0 numAsList ;; 


let process list = 
    List.fold_right (fun x accum -> x + accum) (List.map (fun x -> x * 2) (List.filter (fun x -> x mod 2 = 0) list)) 0;;

print_int (process [1;2;3;4;5;6]);;