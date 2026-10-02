(* Side effects live here: file I/O. Errors come back as values. *)

let save filename store =
  try
    let oc = open_out_bin filename in
    Fun.protect
      ~finally:(fun () -> close_out_noerr oc)   (* closes on every path *)
      (fun () ->
        output_string oc (Store.to_string store);
        flush oc);
    Ok ()
  with Sys_error msg -> Error msg

let load filename =
  try
    let ic = open_in_bin filename in
    let text =
      Fun.protect
        ~finally:(fun () -> close_in_noerr ic)
        (fun () -> really_input_string ic (in_channel_length ic))
    in
    Store.of_string text   (* pure parsing, returns Ok store / Error msg *)
  with Sys_error msg -> Error msg