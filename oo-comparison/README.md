# Object-Oriented Inheritance Comparison

## Overview

This project compares multiple inheritance, diamond inheritance, method resolution, and polymorphism in C++ and Python.

The examples use a personnel hierarchy consisting of `Person`, `Student`, `Employee`, and `TeachingAssistant`. They demonstrate how the two languages handle shared base classes, object state, method overriding, and unrelated types.

## Project Structure

- `cpp/nonvirtual_diamond.cpp` — Demonstrates diamond inheritance without virtual inheritance in C++.
- `cpp/virtual_diamond.cpp` — Demonstrates virtual inheritance, virtual functions, and generic function templates in C++.
- `python/cooperative_diamond.py` — Demonstrates cooperative multiple inheritance, method resolution order (MRO), and duck typing in Python.
- `report.md` — Summarizes the experiments and compares the behavior of C++ and Python.

## Requirements

- A C++ compiler that supports C++20, such as Clang or GCC.
- Python 3.

## Running the C++ Examples

From the `oo-comparison` directory, compile and run the nonvirtual inheritance example:

```bash
clang++ -std=c++20 cpp/nonvirtual_diamond.cpp -o cpp/nonvirtual_diamond
./cpp/nonvirtual_diamond
```

Compile and run the virtual inheritance example:

```bash
clang++ -std=c++20 cpp/virtual_diamond.cpp -o cpp/virtual_diamond
./cpp/virtual_diamond
```

## Running the Python Example

From the `oo-comparison` directory, run:

```bash
python3 python/cooperative_diamond.py
```

## Main Concepts Demonstrated

- Diamond inheritance and duplicate base-class subobjects.
- Virtual inheritance in C++.
- Virtual functions and method overriding.
- Python cooperative initialization using `super()`.
- Python method resolution order (MRO).
- C++ function templates and base-class references.
- Python duck typing.
- How each language handles incompatible types.

See `report.md` for a discussion of the observed results.