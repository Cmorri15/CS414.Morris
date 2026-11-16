# Assignment 08 — Resource Management and Side Effects

## Part A — C++: RAII and Deterministic Destruction

### A1. Unsafe Resource Management

The original code opens a file using `std::fopen()` and stores the result in a raw `FILE*`.

If the program reaches the end of the function normally, it calls `std::fclose()` and releases the file.

However, if an exception occurs inside the loop, execution skips the `std::fclose()` statement. This leaves the file open because there is no automatic cleanup for the raw pointer.

If opening the file fails, no file is acquired, and the function throws an exception.

The original code also uses a fixed-size buffer of 4096 characters. This does not correctly handle arbitrarily long logical lines because one line may be split across multiple reads.

### A2. FileHandle Implementation

I created a `FileHandle` class that owns the file opened by `std::fopen()`.

The constructor opens the file and throws an exception if opening fails. The destructor calls `std::fclose()` when the object is destroyed.

Copy construction, copy assignment, move construction, and move assignment are deleted. This prevents multiple objects from accidentally owning the same file pointer.

The `get()` method returns the `FILE*` without transferring ownership.

### A3. Counting and Forced Failure

The `count_matches_cpp()` function counts the number of lines containing the search string.

It rejects an empty search string before opening the file. It reads characters individually and builds complete lines, allowing it to handle lines longer than 4096 characters.

The function also has an optional parameter that forces an exception after the first complete line. When this happens, the `FileHandle` destructor still runs during exception stack unwinding and closes the file.

### A4. Questions

**1. When does C++ invoke the destructor during normal execution and exception stack unwinding?**

During normal execution, the destructor runs when the `FileHandle` object leaves its scope. If an exception occurs, the destructor runs during stack unwinding as the program exits that scope.

**2. Why is an automatically managed object safer than a raw `FILE*`?**

A raw pointer requires the programmer to remember to close the file manually. If an exception occurs before the close statement, the file can remain open. With RAII, the destructor handles cleanup automatically when the object leaves its scope.

**3. Why is copying a resource-owning handle dangerous? What changes with move semantics or `std::unique_ptr`?**

Copying a raw owning pointer could create two objects that believe they own the same file. Both might attempt to close it, causing a double-close problem.

Move semantics would transfer ownership from one object to another, leaving the original object without ownership. `std::unique_ptr` provides a similar single-owner approach and automatically releases the resource when its owner is destroyed.

**4. Does RAII prevent the file from being opened or prevent the file read from affecting external state?**

No. RAII does not eliminate side effects. The file is still opened and read. RAII manages the responsibility of releasing the resource so that cleanup happens reliably.

---

## Part B — OCaml: Scoped Cleanup with Higher-Order Functions

### B1. Unsafe Pattern

In the original OCaml example, the file is opened using `open_in()`, and the channel is closed only after the counting loop finishes.

If the loop reaches `End_of_file`, that exception is caught by the pattern match and the function returns the count. The program then reaches `close_in()` normally.

However, if another exception occurs inside the loop, such as the simulated failure, it propagates out of the function. The `close_in()` statement is skipped, leaving the channel open.

### B2. with_input_file Helper

I implemented `with_input_file` using `open_in`, `Fun.protect`, and `close_in_noerr`.

The helper opens the file, passes the channel to a callback, and registers a cleanup function that closes the channel.

The cleanup function runs whether the callback returns normally or raises an exception.

The callback should not return the channel or save it for use after the protected computation finishes.

### B3. Counting Function

The `count_matches_ocaml` function performs the same operation as the C++ version.

It checks for an empty search string before opening the file. It uses `input_line` to read complete lines and a substring helper to check whether each line contains the search string.

I used a required Boolean parameter to control the simulated failure. When it is true, the function raises a `Failure` exception after processing the first line.

The exception is allowed to propagate, while `Fun.protect` still runs the cleanup function.

### B4. Cleanup and Garbage Collection

OCaml's garbage collector manages memory, but it does not guarantee that an open file will be closed immediately when a channel is no longer needed.

`Fun.protect` provides cleanup behavior similar to a `try ... finally` construction. The cleanup callback runs after the protected computation finishes, including when an exception occurs.

This differs from C++ because C++ normally ties cleanup to an object's lifetime and destructor. In OCaml, the programmer explicitly defines the protected computation and its cleanup callback.

---

## Part C — Experiments and Comparison

I ran all seven required tests in both C++ and OCaml.

### Test Results

| Test | Description | C++ Result | OCaml Result |
|---|---|---|---|
| T1 | Search sample file for `red` | 2; file closed | 2; file closed |
| T2 | Search sample file for `orange` | 0; file closed | 0; file closed |
| T3 | Search an empty file for `red` | 0; file closed | 0; file closed |
| T4 | Attempt to open a missing file | Opening error reported | Opening error reported |
| T5 | Force an exception after the first line | Exception raised; file closed | Exception raised; file closed |
| T6 | Search using an empty string | Rejected before opening | Rejected before opening |
| T7 | Search a line longer than 4096 characters, with `red` crossing the boundary | 1; file closed | 1; file closed |

### Observations

Both implementations produced the expected results for all seven tests.

For T4, neither program successfully acquired the missing file, so there was no file to close.

For T5, both programs printed their cleanup messages after the simulated exception. This showed that the destructor and the `Fun.protect` cleanup callback ran.

For T6, both programs rejected the empty search string before opening a file.

For T7, I created a file containing a line of 4118 bytes, including the newline. The search string `red` crossed the 4096-character boundary. Both implementations correctly counted the line once.

The cleanup messages show that the cleanup code ran. They are evidence of the program's cleanup behavior, rather than direct proof of operating-system file descriptor release.

### Synthesis Questions

**1. Which operations have side effects? Do the returned counts describe all those effects?**

Opening, reading, and closing files all have side effects because they interact with the file system and operating system. Printing messages and raising exceptions also affect program behavior. The returned count only describes how many lines matched the search string. It does not describe all the other effects that occurred.

**2. In what sense does RAII encapsulate an effect rather than eliminate it?**

RAII does not remove the side effect of opening or reading a file. Instead, it puts responsibility for cleanup inside an object. The object's destructor handles closing the file when the object leaves its scope.

**3. Compare a C++ destructor with an OCaml finally callback. What assumptions must the programmer make?**

A C++ destructor runs when its owning object leaves its scope, including during exception stack unwinding. The programmer must make sure the object actually owns the resource and that its destructor does not throw.

OCaml's `Fun.protect` runs a cleanup callback when the protected computation finishes. The programmer must make sure cleanup is registered immediately after acquiring the resource and that the channel is not used after the protected scope ends.

**4. How do ownership and exception propagation affect correctness?**

In C++, clear ownership ensures that one object is responsible for closing the file. Exceptions do not skip the destructor when the object leaves its scope.

In OCaml, `Fun.protect` ensures that cleanup runs even when an exception propagates out of the callback.

Both approaches improve exception safety by making resource cleanup reliable.

**5. Why is garbage collection not equivalent to deterministic resource cleanup?**

Garbage collection manages memory, but it does not guarantee when an external resource such as a file will be closed. Waiting for garbage collection could leave files open longer than necessary. Explicit cleanup provides more predictable resource management.

An important distinction is that resource cleanup is not the same as rolling back externally visible changes. Neither RAII nor `Fun.protect` automatically undoes something already written to a file or a message already sent over a network.

---

## Part D — Design Extension: OCaml Compositional Resource Handling

I chose Option 2 and implemented `with_two_input_files`.

The function uses nested calls to `with_input_file` to open two files and pass both channels to a callback.

The implementation is:

```ocaml
let with_two_input_files path1 path2 f =
  with_input_file path1 (fun ch1 ->
    with_input_file path2 (fun ch2 ->
      f ch1 ch2))
```

I tested the function by opening `sample.txt` as the first file and attempting to open a missing file as the second file.

The test output showed:

1. The first file opened successfully.
2. Opening the second file failed.
3. The first file was closed.
4. The opening error was reported.

The first file closes because its `Fun.protect` cleanup remains active while the second file is being opened. When the second open raises an exception, that exception propagates outward, causing the first file's cleanup callback to run.

When both files open successfully, the second file closes first, followed by the first file. This is the reverse order of acquisition.

This demonstrates how nested resource-management helpers can be combined while preserving cleanup behavior.

---

## Build and Run Instructions

Run these commands from the `Assignment08` directory.

### C++

Build:

```bash
cmake -S cpp -B cpp/build
cmake --build cpp/build
```

Run:

```bash
./cpp/build/Assignment08
```

### OCaml

Run:

```bash
cd ocaml
dune exec ./main.exe
```

The test programs use relative paths. The C++ program expects to run from the `Assignment08` directory, while the OCaml program expects to run from the `Assignment08/ocaml` directory.

---

## Conclusion

This assignment demonstrated two ways to manage resources safely.

C++ uses RAII and destructors to tie resource cleanup to object lifetime. OCaml uses `Fun.protect` to guarantee that cleanup callbacks run after protected computations.

Both approaches help provide exception safety and prevent resources from being left open when an error occurs. However, neither approach eliminates the side effects of file operations or automatically reverses changes that have already happened.