type 'a gtree =
  | Empty
  | Node of 'a list * 'a gtree list

let rec height (t : 'a gtree) : int =
  match t with
  | Empty -> 0
  | Node (_, children) ->
    1 + List.fold_left (fun acc c -> max acc (height c)) 0 children

let rec preorder (t : 'a gtree) : 'a list =
  match t with
  | Empty -> []
  | Node (keys, children) -> keys @ List.concat_map preorder children

let rec postorder (t : 'a gtree) : 'a list =
  match t with
  | Empty -> []
  | Node (keys, children) -> List.concat_map postorder children @ keys

let rec inorder (t : 'a gtree) : 'a list =
  match t with
  | Empty -> []
  | Node (keys, children) ->
    let rec interleave ks cs =
      match ks, cs with
      | [], [c] -> inorder c
      | k :: ks_rest, c :: cs_rest -> inorder c @ [k] @ interleave ks_rest cs_rest
      | _ -> failwith "malformed gtree: keys/children count mismatch"
    in
    interleave keys children

let rec insert (x : 'a) (t : 'a gtree) : 'a gtree =
  match t with
  | Empty -> Node ([x], [Empty; Empty])
  | Node (keys, children) ->
    let rec find_child_index ks i =
      match ks with
      | [] -> i
      | k :: rest -> if x < k then i else find_child_index rest (i + 1)
    in
    let i = find_child_index keys 0 in
    let children' =
      List.mapi (fun idx c -> if idx = i then insert x c else c) children
    in
    Node (keys, children')

(* Quick tests *)
let () =
  let t = List.fold_left (fun acc x -> insert x acc) Empty [5; 2; 8; 1; 3; 7; 9] in
  Printf.printf "Height: %d\n" (height t);
  Printf.printf "Preorder:  %s\n" (String.concat ", " (List.map string_of_int (preorder t)));
  Printf.printf "Inorder:   %s\n" (String.concat ", " (List.map string_of_int (inorder t)));
  Printf.printf "Postorder: %s\n" (String.concat ", " (List.map string_of_int (postorder t)))