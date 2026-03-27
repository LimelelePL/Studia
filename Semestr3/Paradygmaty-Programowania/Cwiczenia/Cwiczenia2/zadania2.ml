(* zadanie 1*)

let rec normalFibonacci n =
  if n == 0 || n == 1 then n
   else normalFibonacci(n-2) + normalFibonacci (n-1);;

let tailFibonacci n = 
  let rec iter (n, a, b) = 
    if (n<1) then 0
    else if n==0 || n==1 then b
    else iter(n-1, b, b+a) 
  in iter(n, 0, 1);;

print_int(tailFibonacci(6));; 

(*  def root3(a:Double):Double = {

    val ep : Double = 1.0e-15
    val x0 : Double = if math.abs(a)>1 then a/3 else a
    val accuracy: Double => Boolean = (xi : Double) => Math.abs(xi * xi * xi - a) <= ep * Math.abs(a)
    val res: Double => Double = (xi : Double ) => xi + (a/(xi*xi) - xi )/3.0

    @annotation.tailrec
    def iter(result : Double):Double ={ 
        if accuracy(result) then result
        else iter(res(result))
    }
    iter(x0)
  }*)

let root3 a = 
    let ep = 1.0e-15 
  in
    let x0 = if abs_float a > 1.0 then a /. 3.0 else a
  in
    let accuracy xi =
      abs_float (xi *. xi *. xi -. a) <= ep *. abs_float a
  in
    let res xi =
      xi +. (a /. (xi *. xi) -. xi) /. 3.0
  in
    let rec iter result =
      if accuracy result then result
      else iter (res result)
  in
  iter x0;;


(*  zadanie 4  *)
let [_; _; x; _; _] = [-2; -1; 0; 2; 2];;
let [-2; _; x; 2; 2] = [-2; -1; 0; 2; 2];;
let _ :: _ :: x :: _ :: _ :: [] = [-2; -1; 0; 2; 2];;

let [_ ;  ] = [ (1,2); (0,1) ]
let [(1,2) ; (x, _)] = [ (1,2); (0,1) ]

let rec initSegment (xs, ys) =
  match (xs, ys) with
  | ([], _) -> true
  | (_, []) -> false
  | (h1::t1, h2::t2) when h1 = h2 -> initSegment (t1, t2)
  | _ -> false
;;


let rec replaceNth (list, position, elem) =
  match (list, position) with
  | ([], _) -> list                                 
  | (h :: t, 0) -> elem :: t
  | (h :: t, _) -> h :: replaceNth (t, position - 1, elem);;

let test = replaceNth([1;2;3;4;5;6], 3, 10);;
