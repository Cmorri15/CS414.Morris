(* A zipper list: items left of the focus (stored nearest-first, i.e.
   reversed), the focus itself, and items right of the focus (in order). *)
type 'a t =
  | Empty
  | Zipper of 'a list * 'a * 'a list

let empty_list : 'a t = Empty

(* Predicate: is the list empty? *)
let empty (z : 'a t) : bool =
  match z with
  | Empty -> true
  | Zipper _ -> false

(* Move focus one entry left; does nothing at the left end. *)
let move_left (z : 'a t) : 'a t =
  match z with
  | Zipper (l :: ls, x, rs) -> Zipper (ls, l, x :: rs)
  | _ -> z

(* Move focus one entry right; does nothing at the right end. *)
let move_right (z : 'a t) : 'a t =
  match z with
  | Zipper (ls, x, r :: rs) -> Zipper (x :: ls, r, rs)
  | _ -> z

(* Add an item at the very front of the whole list.
   The focus stays where it was. On an empty list, the new item becomes the focus. *)
let push_front (v : 'a) (z : 'a t) : 'a t =
  match z with
  | Empty -> Zipper ([], v, [])
  | Zipper (ls, x, rs) -> Zipper (ls @ [ v ], x, rs)

(* Add an item at the very back of the whole list.
   The focus stays where it was. *)
let push_back (v : 'a) (z : 'a t) : 'a t =
  match z with
  | Empty -> Zipper ([], v, [])
  | Zipper (ls, x, rs) -> Zipper (ls, x, rs @ [ v ])

(* Helper: last element of a list, or None if the list is empty. *)
let rec last = function
  | [] -> None
  | [ x ] -> Some x
  | _ :: tl -> last tl

(* First item of the whole list.
   The left list is reversed, so the front is the last item of ls.
   If ls is empty, the focus is the front. *)
let front (z : 'a t) : 'a option =
  match z with
  | Empty -> None
  | Zipper (ls, x, _) -> (match last ls with None -> Some x | some -> some)

(* Last item of the whole list.
   If rs is empty, the focus is the back. *)
let back (z : 'a t) : 'a option =
  match z with
  | Empty -> None
  | Zipper (_, x, rs) -> (match last rs with None -> Some x | some -> some)

(* Item under the focus. *)
let focus (z : 'a t) : 'a option =
  match z with
  | Empty -> None
  | Zipper (_, x, _) -> Some x

(* Helper for testing: the whole list in order. *)
let to_list (z : 'a t) : 'a list =
  match z with
  | Empty -> []
  | Zipper (ls, x, rs) -> List.rev ls @ (x :: rs)