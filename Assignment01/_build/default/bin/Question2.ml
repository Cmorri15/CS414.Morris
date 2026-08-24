type 'a tree =
  | Leaf
  | Node of 'a tree * 'a * 'a tree

let rec height (t : 'a tree) : int =
  match t with
  | Leaf -> 0
  | Node (l, _, r) -> 1 + max (height l) (height r)

let rec prune (t : 'a tree) : 'a tree =
  match t with
  | Leaf -> Leaf
  | Node (Leaf, _, Leaf) -> Leaf
  | Node (l, x, r) -> Node (prune l, x, prune r)

let level_traversal (t : 'a tree) : 'a list =
  let rec aux (frontier : 'a tree list) : 'a list =
    match frontier with
    | [] -> []
    | _ ->
      let values = List.filter_map
        (function Leaf -> None | Node (_, x, _) -> Some x)
        frontier
      in
      let next_frontier = List.concat_map
        (function Leaf -> [] | Node (l, _, r) -> [l; r])
        frontier
      in
      values @ aux next_frontier
  in
  aux [t]

(* Quick tests *)
let sample : int tree =
  Node (Node (Leaf, 1, Leaf), 2, Node (Node (Leaf, 4, Leaf), 3, Leaf))

let () =
  Printf.printf "Level traversal: %s\n"
    (String.concat ", " (List.map string_of_int (level_traversal sample)));
  Printf.printf "Height: %d\n" (height sample);
  Printf.printf "Height after prune: %d\n" (height (prune sample))