module StringMap = Map.Make (String)

type t = string StringMap.t

let empty : t = StringMap.empty

(* Let-binding operator so validated operations chain without nested matches. *)
let ( let* ) = Result.bind

(* ---------- Pure core operations ---------- *)

let valid_text s =
  not (String.exists (fun c -> c = '\t' || c = '\n' || c = '\r') s)

(* Returns a NEW store; the argument is never modified.
   Validation mirrors the C++ version, so failure is a value (Error),
   not an exception. *)
let set key value store =
  if key = "" then Error "key must be non-empty"
  else if not (valid_text key && valid_text value) then
    Error "key/value may not contain tabs or newlines"
  else Ok (StringMap.add key value store)

let get key store = StringMap.find_opt key store

let mem key store = StringMap.mem key store

let delete key store = StringMap.remove key store

(* Sorted (key, value) pairs. *)
let list store = StringMap.bindings store

let size store = StringMap.cardinal store

(* ---------- Pure transaction helper ---------- *)

(* Run [operation] on [store]. On Ok, use the new store; on Error, keep
   the original. Rollback needs no restore step because [store] was
   never modified. *)
let transaction operation store =
  match operation store with
  | Ok new_store -> new_store
  | Error _ -> store

(* ---------- Pure serialization (no file I/O here) ---------- *)

let to_string store =
  list store
  |> List.map (fun (k, v) -> k ^ "\t" ^ v ^ "\n")
  |> String.concat ""

let of_string text =
  let parse_line acc line =
    let* m = acc in
    if line = "" then Ok m
    else
      match String.index_opt line '\t' with
      | Some i when i > 0 ->
          let key = String.sub line 0 i in
          let value = String.sub line (i + 1) (String.length line - i - 1) in
          Ok (StringMap.add key value m)
      | _ -> Error ("malformed line: " ^ line)
  in
  String.split_on_char '\n' text |> List.fold_left parse_line (Ok empty)