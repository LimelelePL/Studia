let rec sum list =    
 if list = [] then [] else (    
match List.hd list with 
 | (a,b) -> (a+b) :: sum (List.tl list)    
 | (a,_) -> a:: sum (List.tl list)    
 | (_,b) -> b :: sum (List.tl list)    
 | (_,_) -> 0:: sum (List.tl list)    
)    
;;

let result = sum([(1,2);(2,3);(4,3)]);;