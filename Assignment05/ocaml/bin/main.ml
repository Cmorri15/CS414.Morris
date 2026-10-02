open Kvlib

(* Split "WORD rest of line" into ("WORD", "rest of line"). *)
let split_first s =
  let s = String.trim s in
  match String.index_opt s ' ' with
  | None -> (s, "")
  | Some i ->
      ( String.sub s 0 i,
        String.trim (String.sub s (i + 1) (String.length s - i - 1)) )

(* Console output happens here. Returns the next (store, tx), or None to quit.
   [tx] is [Some original] while a transaction is open. *)
let handle store tx cmd key value =
  let same = Some (store, tx) in
  match String.uppercase_ascii cmd with
  | "" -> same
  | "SET" ->
      if key = "" then (print_endline "usage: SET key value"; same)
      else (
        match Store.set key value store with
        | Ok s -> Some (s, tx)
        | Error e -> print_endline ("error: " ^ e); same)
  | "GET" ->
      if key = "" then (print_endline "usage: GET key"; same)
      else (
        (match Store.get key store with
         | Some v -> print_endline v
         | None -> print_endline "(not found)");
        same)
  | "DELETE" ->
      if key = "" then (print_endline "usage: DELETE key"; same)
      else if Store.mem key store then Some (Store.delete key store, tx)
      else (print_endline "(not found)"; same)
  | "LIST" ->
      List.iter (fun (k, v) -> Printf.printf "%s = %s\n" k v) (Store.list store);
      same
  | "SAVE" ->
      if key = "" then (print_endline "usage: SAVE filename"; same)
      else (
        (match Storage.save key store with
         | Ok () -> ()
         | Error e -> print_endline ("error: " ^ e));
        same)
  | "LOAD" ->
      if key = "" then (print_endline "usage: LOAD filename"; same)
      else (
        match Storage.load key with
        | Ok s -> Some (s, tx)
        | Error e -> print_endline ("error: " ^ e); same)
  | "BEGIN" -> (
      match tx with
      | Some _ -> print_endline "transaction already open"; same
      | None -> Some (store, Some store))   (* "snapshot" is just a reference *)
  | "COMMIT" -> (
      match tx with
      | None -> print_endline "no open transaction"; same
      | Some _ -> Some (store, None))
  | "ABORT" -> (
      match tx with
      | None -> print_endline "no open transaction"; same
      | Some original -> Some (original, None))   (* rollback = use the old value *)
  | "QUIT" -> None
  | other -> print_endline ("unknown command: " ^ other); same

let rec loop store tx =
  print_string "> ";
  flush stdout;
  match try Some (input_line stdin) with End_of_file -> None with
  | None -> ()
  | Some line -> (
      let cmd, rest = split_first line in
      let key, value = split_first rest in
      match handle store tx cmd key value with
      | None -> ()
      | Some (store', tx') -> loop store' tx')

let () = loop Store.empty None