"""
Caleb Morris
Assignment05

Step 2: Tokenizer

This tokenizer extends the Assignment03 shell tokenizer to support:

    SET commands
    echo commands
    variables beginning with $
    assignment operator =
    arithmetic operators + - * /
    parentheses

Variables have the form:

    $x
    $name
    $count1

A variable must begin with '$' followed by a letter. The remaining
characters may be letters or digits.

Whitespace is ignored.
"""


KEYWORDS = {
    "ls",
    "cd",
    "cat",
    "print",
    "exec",
    "set",
    "echo",
}


class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value!r})"

    def __eq__(self, other):
        return (
            isinstance(other, Token)
            and self.type == other.type
            and self.value == other.value
        )


class LexError(Exception):
    """Raised when the tokenizer encounters invalid input."""
    pass


def tokenize(line):
    """
    Convert a raw command-line string into a list of Token objects.

    The list always ends with an EOF token.

    Raises LexError when invalid input is encountered.
    """

    tokens = []
    i = 0
    n = len(line)

    while i < n:
        c = line[i]

        # ---------------------------------------------------------
        # Whitespace
        # ---------------------------------------------------------
        if c.isspace():
            i += 1
            continue

        # ---------------------------------------------------------
        # ROOT
        # ---------------------------------------------------------
        if c == '\\':
            tokens.append(Token("ROOT", "\\"))
            i += 1
            continue

        # ---------------------------------------------------------
        # VARIABLE
        #
        # VARIABLE ::= "$" IDENTIFIER
        # ---------------------------------------------------------
        if c == '$':
            start = i
            i += 1

            # A variable must have a letter immediately after '$'
            if i >= n or not line[i].isalpha():
                raise LexError(
                    "Variable must begin with '$' followed by a letter"
                )

            # First character of identifier
            i += 1

            # Remaining identifier characters
            while i < n and line[i].isalnum():
                i += 1

            variable = line[start:i]

            tokens.append(Token("VARIABLE", variable))
            continue

        # ---------------------------------------------------------
        # Assignment and arithmetic operators
        # ---------------------------------------------------------
        if c == '=':
            tokens.append(Token("EQUALS", "="))
            i += 1
            continue

        if c == '+':
            tokens.append(Token("PLUS", "+"))
            i += 1
            continue

        if c == '-':
            tokens.append(Token("MINUS", "-"))
            i += 1
            continue

        if c == '*':
            tokens.append(Token("MULTIPLY", "*"))
            i += 1
            continue

        if c == '/':
            tokens.append(Token("DIVIDE", "/"))
            i += 1
            continue

        if c == '(':
            tokens.append(Token("LEFT_PAREN", "("))
            i += 1
            continue

        if c == ')':
            tokens.append(Token("RIGHT_PAREN", ")"))
            i += 1
            continue

        # ---------------------------------------------------------
        # Words, filenames, and folder names
        # ---------------------------------------------------------
        if c.isalpha():
            start = i

            while i < n and line[i].isalnum():
                i += 1

            word = line[start:i]

            # -----------------------------------------------------
            # Filename
            # -----------------------------------------------------
            if i < n and line[i] == '.':
                i += 1

                ext_start = i

                while i < n and line[i].isalnum():
                    i += 1

                ext = line[ext_start:i]

                # Filename must be exactly 8 chars . 3 chars
                if len(word) == 8 and len(ext) == 3:
                    tokens.append(
                        Token("FILENAME", f"{word}.{ext}")
                    )
                else:
                    raise LexError(
                        f"Malformed filename '{word}.{ext}': "
                        f"expected 8 characters + '.' + 3 characters"
                    )

                # There cannot be junk immediately after filename
                if i < n and not line[i].isspace():
                    raise LexError(
                        f"Unexpected character '{line[i]}' "
                        f"after filename"
                    )

                continue

            # -----------------------------------------------------
            # Keyword
            # -----------------------------------------------------
            if word.lower() in KEYWORDS:
                tokens.append(
                    Token(word.upper(), word)
                )
                continue

            # -----------------------------------------------------
            # Folder name
            # -----------------------------------------------------
            if 1 <= len(word) <= 8:
                tokens.append(
                    Token("FOLDERNAME", word)
                )
                continue

            raise LexError(
                f"Malformed folder name '{word}': "
                f"expected 1 to 8 characters"
            )

        # ---------------------------------------------------------
        # Anything else is invalid
        # ---------------------------------------------------------
        raise LexError(
            f"Unexpected character '{c}' at position {i}"
        )

    tokens.append(Token("EOF", None))
    return tokens


# -------------------------------------------------------------------
# Manual tokenizer tests
# -------------------------------------------------------------------

if __name__ == "__main__":

    valid_tests = [
        "ls",
        "ls MYDOCS",
        "cd",
        "cd MYDOCS",
        "cd \\",
        "cat REPORT12.TXT",
        "print REPORT12.TXT",
        "exec PROGRAM1.EXE",

        "SET $x = hello",
        "SET $name = Caleb",
        "SET $count1 = 10",
        "echo $x",

        "SET $x = $y",
        "SET $x = $y + $z",
        "SET $x = $a * $b",
        "SET $x = ($a + $b)",
        "SET $x = $a + $b * $c",
    ]

    invalid_tests = [
        "$",
        "$123",
        "$_name",
        "SET $ = hello",
        "SET $123abc = hello",
    ]

    print("=== Valid commands ===")

    for cmd in valid_tests:
        try:
            print(f"{cmd!r:35} -> {tokenize(cmd)}")
        except LexError as e:
            print(f"{cmd!r:35} -> ERROR: {e}")

    print("\n=== Invalid commands ===")

    for cmd in invalid_tests:
        try:
            result = tokenize(cmd)
            print(
                f"{cmd!r:35} -> {result} "
                f"(WARNING: expected error)"
            )
        except LexError as e:
            print(f"{cmd!r:35} -> LexError: {e}")