# Q2: Zipper List in OCaml

## The type

    type 'a t = Empty | Zipper of 'a list * 'a * 'a list

A zipper list is either `Empty` or a `Zipper` holding three things: the list of
items to the left of the focus, the focus item itself, and the list of items to
the right of the focus. The `'a` makes it a parametric type, so it works for
ints, strings, or any other type.

## Operations

- `empty`: returns true if the list is empty
- `move_left`: moves the focus one entry to the left
- `move_right`: moves the focus one entry to the right
- `push_front`: adds an item to the front of the list
- `push_back`: adds an item to the back of the list
- `front`: returns the item at the front of the list
- `back`: returns the item at the back of the list
- `focus`: returns the item at the current focus
- `to_list`: helper that returns the whole list in order (used for testing)

## Design decisions

- The left list is stored reversed, so the item next to the focus is at its
  head. This makes `move_left` and `move_right` O(1).
- Moving past either end of the list does nothing.
- `focus`, `front`, and `back` return an `option`, with `None` for an empty list.
- `push_front` and `push_back` leave the focus where it was. On an empty list,
  the pushed item becomes the focus.
- `push_front`, `push_back`, `front`, and `back` are O(n) because they have to
  walk to the far end of a list.

## Build and run

    ocamlfind ocamlopt zipper.ml test_zipper.ml -o test_zipper
    ./test_zipper

Expected output: `All zipper tests passed.`

## Test data

`test_zipper.ml` contains the tests. It checks the empty list, pushing, moving
in both directions, boundary behavior, and a list of strings to show the type
is parametric.