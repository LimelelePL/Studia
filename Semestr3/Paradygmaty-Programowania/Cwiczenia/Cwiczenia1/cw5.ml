
let rec isPalindrome list = list = List.rev list;;
let p = isPalindrome [2;1;1;2];;



let rec listLength list = 
 if list = [] then 0
 else 1 + listLength (List.tl list);;

let len = listLength([1;2;3]);;
print_int(len)

