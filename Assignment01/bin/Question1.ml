type nat =
  | Z
  | S of nat

let rec to_int : nat -> int = function
  | Z -> 0
  | S n -> 1 + to_int n

let rec add (x : nat) (y : nat) : nat =
  match x with
  | Z -> y
  | S x_prev -> S (add x_prev y)

(* Multiplication: x * 0 = 0 ; x * S(y) = x + (x * y) *)
let rec mult (x : nat) (y : nat) : nat =
  match y with
  | Z -> Z
  | S y_prev -> add x (mult x y_prev)

(* Truncated subtraction, needed for division *)
let rec sub (x : nat) (y : nat) : nat =
  match y with
  | Z -> x
  | S y_prev ->
    match x with
    | Z -> Z
    | S x_prev -> sub x_prev y_prev

(* x <= y ? *)
let rec leq (x : nat) (y : nat) : bool =
  match x, y with
  | Z, _ -> true
  | S _, Z -> false
  | S x_prev, S y_prev -> leq x_prev y_prev

(* Division by repeated subtraction: how many times does y fit into x? *)
let rec div (x : nat) (y : nat) : nat =
  match y with
  | Z -> failwith "division by zero"
  | _ -> if leq y x then S (div (sub x y) y) else Z

  (* Quick tests *)
let () =
  Printf.printf "2 * 3 = %d\n" (to_int (mult (S (S Z)) (S (S (S Z)))));
  Printf.printf "7 / 2 = %d\n" (to_int (div (S(S(S(S(S(S(S Z))))))) (S (S Z))))