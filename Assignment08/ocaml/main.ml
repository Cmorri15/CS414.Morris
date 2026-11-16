
let with_input_file path f =
  let ch = open_in path in
  print_endline ("File opened: " ^ path);

  Fun.protect
    ~finally:(fun () ->
      close_in_noerr ch;
      print_endline "File closed")
    (fun () -> f ch)

let with_two_input_files path1 path2 f =
  with_input_file path1 (fun ch1 ->
    with_input_file path2 (fun ch2 ->
      f ch1 ch2))


let contains line needle =
  let line_length = String.length line in
  let needle_length = String.length needle in

  let rec check position =
    if position + needle_length > line_length then
      false
    else if String.sub line position needle_length = needle then
      true
    else
      check (position + 1)
  in

  check 0


let count_matches_ocaml path needle fail_after_first_line =
  if needle = "" then
    invalid_arg "Search string cannot be empty";

  with_input_file path (fun ch ->
    let rec count_lines count =
      match input_line ch with
      | line ->
          let count =
            if contains line needle then count + 1
            else count
          in

          if fail_after_first_line then
            failwith "simulated failure";

          count_lines count

      | exception End_of_file -> count
    in

    count_lines 0
  )


let () =
  let path = "../data/sample.txt" in

  try
    Printf.printf "Matches for red: %d\n"
      (count_matches_ocaml path "red" false);

    Printf.printf "Matches for orange: %d\n"
      (count_matches_ocaml path "orange" false);

    Printf.printf "Matches for empty file: %d\n"
      (count_matches_ocaml "../data/empty.txt" "red" false);

    (try
       ignore (count_matches_ocaml "../data/missing.txt" "red" false)
     with
     | Sys_error message ->
         Printf.printf "Missing file: %s\n" message);

    (try
       ignore (count_matches_ocaml path "" false)
     with
     | Invalid_argument message ->
         Printf.printf "Empty needle: %s\n" message);

    Printf.printf "Matches for long line: %d\n"
      (count_matches_ocaml "../data/long.txt" "red" false);

    print_endline "Testing two-file cleanup:";

    (try
       with_two_input_files "../data/sample.txt" "../data/missing.txt"
         (fun _ _ -> print_endline "Both files opened")
     with
     | Sys_error message ->
         Printf.printf "Second file failed: %s\n" message);

    print_endline "Testing forced failure:";

    ignore (count_matches_ocaml path "red" true)

  with
  | Invalid_argument message ->
      Printf.printf "Error: %s\n" message
  | Failure message ->
      Printf.printf "Error: %s\n" message
  | Sys_error message ->
      Printf.printf "Error: %s\n" message
