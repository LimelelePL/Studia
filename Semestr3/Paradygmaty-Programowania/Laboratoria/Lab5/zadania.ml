

type eval = Num of float | Add | Sub | Mul | Div;;

let evaluate list = 
    let pop stack =
        match stack with
        | head :: tail -> (head, tail)
        | [] -> failwith "pusty stos - nieprawidłowa ilosc argumentów!" 

      in 
    let push stack elem = elem :: stack
   in
    let rec helper list stack = 
    match list with
    | head :: tail ->
        (
        match head with
            | Num number -> helper tail (push stack number)
            | Add ->
               let (num1, st1) = pop stack in
               let (num2, st2) = pop st1 in
               helper tail (push st2 (num2 +. num1))
               
            | Sub ->
               let (num1, st1) = pop stack in
               let (num2, st2) = pop st1 in
               helper tail (push st2 (num2 -. num1))

            | Mul ->
              let (num1, st1) = pop stack in 
              let (num2, st2) = pop st1 in
              helper tail (push st2 (num2 *. num1))

            | Div -> 
              let (num1, st1) = pop stack in 
              let (num2, st2) = pop st1 in 
              if num1 = 0. then failwith "dzielenie przez 0"
               else helper tail (push st2 (num2 /. num1))
        )
        (*jezeli nasza lista bedzie pusta oznacza to ze wszystkie operacje zostaly przetworzone i
                    i jedynym elementem na stosie powinien być wynik wszystkich operacji *)
        | [] -> 
            (
            match stack with
            | head :: [] -> head
            | _ -> failwith "nieprawidlowa ilosc argumentow"
            )
    in helper list [];;

    (*TESTy*)
  let print_test name expr =
  let result =
    try
      let r = evaluate expr in
      Printf.sprintf "%.2f" r
    with Failure msg ->
      Printf.sprintf "Błąd: %s" msg
  in
  Printf.printf "%s = %s\n" name result
;;

print_test "test 1: 2 + (5+3) - Lista [5,3,+,2,+]"
  [Num 5.; Num 3.; Add; Num 2.; Add];

print_test "test 2: 6/(5-5) - Lista [5,5,-, 6,/]"
  [Num 6.; Num 5.; Num 5.; Sub; Div];;

print_test "test 3: Lista [+ * 1 / ]"
  [Add; Mul; Num 1.; Div];

print_test "test 4: Lista []"
  [Add];


  