# Assignment 02 Writeup

## Question 2: Parse Trees

Grammar:

    Expr   → Expr + Term | Expr - Term | Term
    Term   → Term * Factor | Term / Factor | Factor
    Factor → ( Expr ) | number | identifier

### 1. (a+(b*C)/2)

    Factor
    └── ( Expr )
          Expr → Expr + Term
          ├── Expr → Term → Factor → identifier: a
          └── Term → Term / Factor
                ├── Term → Factor → ( Expr )
                │           Expr → Term → Term * Factor
                │                  ├── Term → Factor → identifier: b
                │                  └── Factor → identifier: C
                └── Factor → number: 2

### 2. a*(3+b)*4

    Term → Term * Factor
    ├── Term → Term * Factor
    │         ├── Term → Factor → identifier: a
    │         └── Factor → ( Expr )
    │                    Expr → Expr + Term
    │                    ├── Expr → Term → Factor → number: 3
    │                    └── Term → Factor → identifier: b
    └── Factor → number: 4

### 3. 42*c+3*(a+b)

    Expr → Expr + Term
    ├── Expr → Term → Term * Factor
    │         ├── Term → Factor → number: 42
    │         └── Factor → identifier: c
    └── Term → Term * Factor
              ├── Term → Factor → number: 3
              └── Factor → ( Expr )
                         Expr → Expr + Term
                         ├── Expr → Term → Factor → identifier: a
                         └── Term → Factor → identifier: b

## Question 3: Extended Grammar

New grammar with unary + and -:

    Expr   → Expr + Term | Expr - Term | Term
    Term   → Term * Unary | Term / Unary | Unary
    Unary  → + Unary | - Unary | Factor
    Factor → ( Expr ) | number | identifier

Unary sits between Term and Factor so that unary +/- bind more tightly
than * and /, but still resolve down to a Factor (number, identifier,
or parenthesized expression). It is right-recursive so that stacked
signs (e.g. --3) apply outward from the innermost value.

### Parse tree for (3+-3)*4

    Term → Term * Factor
    ├── Term → Unary → Factor → ( Expr )
    │                          Expr → Expr + Term
    │                          ├── Expr → Term → Unary → Factor → number: 3
    │                          └── Term → Unary → - Unary → Factor → number: 3
    └── Factor → number: 4