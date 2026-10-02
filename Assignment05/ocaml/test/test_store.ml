open Kvlib

let failures = ref 0

let check name cond =
  if not cond then (
    incr failures;
    Printf.eprintf "FAIL: %s\n" name)

let ( let* ) = Result.bind
let ok = function Ok x -> x | Error e -> failwith e
let is_error = function Error _ -> true | Ok _ -> false

let test_set_get () =
  let s = ok (Store.set "name" "Ada" Store.empty) in
  check "get after set" (Store.get "name" s = Some "Ada");
  let s2 = ok (Store.set "name" "Grace" s) in
  check "overwrite" (Store.get "name" s2 = Some "Grace");
  check "missing" (Store.get "nope" s = None)

let test_delete () =
  let s = ok (Store.set "a" "1" Store.empty) in
  let s2 = Store.delete "a" s in
  check "deleted" (Store.get "a" s2 = None);
  check "delete missing is harmless" (Store.size (Store.delete "zzz" s2) = 0)

let test_list_sorted () =
  let s = ok (Store.set "b" "2" Store.empty) in
  let s = ok (Store.set "a" "1" s) in
  check "sorted list" (Store.list s = [ ("a", "1"); ("b", "2") ])

let test_invalid () =
  check "empty key" (is_error (Store.set "" "v" Store.empty));
  check "tab in value" (is_error (Store.set "k" "a\tb" Store.empty))

(* Immutability: old values stay usable after "modification". *)
let test_old_state_retained () =
  let original = ok (Store.set "x" "10" Store.empty) in
  let modified = ok (Store.set "x" "20" original) in
  check "original untouched" (Store.get "x" original = Some "10");
  check "modified has new" (Store.get "x" modified = Some "20")

let test_transaction_abort () =
  let initial = ok (Store.set "x" "10" Store.empty) in
  let operation s =
    let* s = Store.set "x" "20" s in
    let* s = Store.set "y" "30" s in
    ignore s;
    Error "abort"
  in
  let final = Store.transaction operation initial in
  check "x restored" (Store.get "x" final = Some "10");
  check "y absent" (Store.get "y" final = None)

let test_transaction_failure_midway () =
  let initial = ok (Store.set "x" "10" Store.empty) in
  let operation s =
    let* s = Store.set "x" "20" s in
    Store.set "" "bad" s   (* fails *)
  in
  let final = Store.transaction operation initial in
  check "rolled back on error" (Store.get "x" final = Some "10")

let test_transaction_commit () =
  let initial = ok (Store.set "x" "10" Store.empty) in
  let operation s =
    let* s = Store.set "x" "20" s in
    Store.set "y" "30" s
  in
  let final = Store.transaction operation initial in
  check "x updated" (Store.get "x" final = Some "20");
  check "y added" (Store.get "y" final = Some "30")

let test_save_load () =
  let s = ok (Store.set "name" "Ada Lovelace" Store.empty) in
  let s = ok (Store.set "language" "OCaml" s) in
  let path = Filename.temp_file "kv_test" ".txt" in
  check "save ok" (Storage.save path s = Ok ());
  (match Storage.load path with
   | Ok loaded -> check "round trip" (Store.list loaded = Store.list s)
   | Error e -> check ("load failed: " ^ e) false);
  Sys.remove path

let test_load_errors () =
  check "missing file" (is_error (Storage.load "/no/such/file.txt"));
  check "malformed text" (is_error (Store.of_string "no tab here\n"))

let () =
  test_set_get ();
  test_delete ();
  test_list_sorted ();
  test_invalid ();
  test_old_state_retained ();
  test_transaction_abort ();
  test_transaction_failure_midway ();
  test_transaction_commit ();
  test_save_load ();
  test_load_errors ();
  if !failures = 0 then print_endline "All OCaml tests passed"
  else exit 1