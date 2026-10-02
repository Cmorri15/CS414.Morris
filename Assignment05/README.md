# Assignment 05: Transactional Key-Value Store (C++ and OCaml)

Two implementations of the same store. Commands: SET, GET, DELETE, LIST,
SAVE, LOAD, QUIT, plus BEGIN / COMMIT / ABORT for transactions.
Save files are plain text, one `key<TAB>value` pair per line, and are
compatible between the two programs. Keys and values may not contain
tabs or newlines.

## C++ (requires CMake and a C++20 compiler)
```bash
cd cpp
cmake -S . -B build
cmake --build build
./build/kvstore
ctest --test-dir build --output-on-failure
```

## OCaml (requires opam and dune)
```bash
cd ocaml
dune build
dune exec ./bin/main.exe
dune test --force
```

## Sample data
`data/sample.txt` was written by `SAVE` and can be loaded by either program:
`LOAD ../data/sample.txt`

## Comparison
See `COMPARISON.md`.