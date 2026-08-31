type 'a rose = Node of 'a * 'a rose list

let rec size (t : 'a rose) : int =
  match t with
  | Node (_, children) -> 1 + List.fold_left (fun acc c -> acc + size c) 0 children

let rec map (f : 'a -> 'b) (t : 'a rose) : 'b rose =
  match t with
  | Node (x, children) -> Node (f x, List.map (map f) children)

let rec fold (f : 'a -> 'b list -> 'b) (t : 'a rose) : 'b =
  match t with
  | Node (x, children) -> f x (List.map (fold f) children)

let sample : int rose =
  Node (1, [Node (2, [Node (5, [])]); Node (3, []); Node (4, [])])

let () =
  Printf.printf "Size: %d\n" (size sample);
  let doubled = map (fun x -> x * 2) sample in
  Printf.printf "Sum of doubled tree: %d\n"
    (fold (fun x cs -> x + List.fold_left (+) 0 cs) doubled)