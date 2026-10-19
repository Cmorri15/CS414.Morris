open Zipper

let () =
  assert (empty empty_list);
  assert (focus empty_list = None);
  assert (front empty_list = None);
  assert (back empty_list = None);

  let z = empty_list |> push_back 1 |> push_back 2 |> push_back 3 in
  assert (not (empty z));
  assert (to_list z = [1; 2; 3]);
  assert (focus z = Some 1);
  assert (front z = Some 1);
  assert (back z = Some 3);

  let z = move_right z in
  assert (focus z = Some 2);
  let z = push_front 0 z in
  assert (to_list z = [0; 1; 2; 3]);
  assert (front z = Some 0);
  assert (focus z = Some 2);

  let z = push_back 4 z in
  assert (to_list z = [0; 1; 2; 3; 4]);
  assert (back z = Some 4);

  let z = z |> move_left |> move_left in
  assert (focus z = Some 0);
  assert (focus (move_left z) = Some 0);

  let z = List.fold_left (fun z _ -> move_right z) z [1;2;3;4;5] in
  assert (focus z = Some 4);

  let s = empty_list |> push_back "a" |> push_back "b" |> move_right in
  assert (focus s = Some "b");

  print_endline "All zipper tests passed."