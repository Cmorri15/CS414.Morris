# Comparison: C++ and OCaml

## Side effects

In C++, `Store::set`, `remove`, and `load` mutate `data_` in place, `save`
writes a file, and `main.cpp` performs all console I/O. `Transaction`'s
constructor copies the store, and its destructor writes to the store
(rollback), so object lifetime itself triggers an effect.

In OCaml, the effects are the file operations in `Storage.save` and
`Storage.load` and the console reads and writes in `main.ml`. Everything in
`store.ml` is free of side effects. Pure functions are `set`, `get`, `mem`,
`delete`, `list`, `size`, `to_string`, `of_string`, and `transaction`
(`transaction` is pure as long as the operation passed to it is pure).
Even file formatting and parsing are pure string conversions, so `Storage`
only has to move one string to or from disk.

## Mutable state

In C++ the main mutable state is `Store::data_`. There is also
`Transaction::committed_`, the file streams, and the
`std::optional<Transaction>` in `main`. In OCaml the core has no mutable
state. The "current store" exists only as an argument passed from one call
of `loop` to the next. The only mutable things are the OS-level channels
(stdin, stdout, files) and a `failures` counter in the tests.

## RAII versus immutability

RAII ties an effect to a scope. The `ofstream` and `ifstream` objects close
their files on every exit path, including exceptions, and `Transaction`
rolls back whenever it is destroyed uncommitted. This makes cleanup
automatic, but the mutation is still happening. RAII controls when
effects are undone; it does not remove them.

Immutability reduces the number of effects that exist. Because `set`
returns a new store, there is nothing to undo, and the unavoidable effects
(I/O) sit in identifiable modules. `Fun.protect` provides RAII-like
cleanup for files, but the programmer must ask for it explicitly, while in
C++ it comes from the type.

## Rollback

In C++, rollback means restoring a saved copy. The constructor copies the
whole map into `backup_`, which costs O(n) time and memory. If `commit()`
is not called, the destructor moves the backup back over the store. The
benefit is that this works on exception paths without any `catch` block.

In OCaml, rollback is not an operation. `BEGIN` keeps a reference to the
current store, and `ABORT` just continues using that reference. The
`transaction` helper is one `match`: on `Ok` use the new store, on `Error`
keep the old one.

## Why OCaml can keep old states cheaply

`Map` is a persistent balanced tree. `add` copies only the path from the
root to the changed node, O(log n) nodes, and the new tree shares every
other subtree with the old one. The old map stays valid because nothing
ever modifies a node after it is built, so sharing is safe. No full copy
is needed.

## Which model made rollback easier?

The OCaml model, because of its mechanism rather than its syntax. When
values never change, "the state before the transaction" is simply a value
that is still in scope, so keeping it costs nothing and restoring it is
reassignment. In C++, mutation destroys the old state, so the program must
preserve it deliberately (the copy) and restore it deliberately (the
destructor). RAII makes that second part reliable and exception-safe, which
is a real strength, and in C++ it is the idiomatic solution. But it is
machinery built to compensate for in-place mutation, while OCaml's
immutability avoids the problem in the first place.

A trade-off applies: C++ can mutate in place with no allocation for each
update, which is faster in the common case, and RAII generalizes to
resources that are not data (files, locks, sockets). Immutable values
handle state well but still need explicit handling for external effects.