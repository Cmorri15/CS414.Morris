"""
Caleb Morris
Assignment03
This is the step two of this assignment. I did have the help of Claude.ai when completing this assingment.

Step 2: Tokenizer

Grammar reference
    command    ::= ls_cmd | cd_cmd | cat_cmd | print_cmd | exec_cmd
    ls_cmd     ::= "ls" [ FILENAME | FOLDERNAME ]
    cd_cmd     ::= "cd" [ FOLDERNAME | ROOT ]
    cat_cmd    ::= "cat" FILENAME
    print_cmd  ::= "print" FILENAME
    exec_cmd   ::= "exec" FILENAME

    FILENAME   ::= 8 letters "." 3 letters
    FOLDERNAME ::= 1 to 8 letters (no dot)
    ROOT       ::= "\"

Tokens produced: LS, CD, CAT, PRINT, EXEC, FILENAME, FOLDERNAME, ROOT, EOF
Whitespace is consumed and never emitted as a token.
Malformed names (wrong length / wrong dot placement) are rejected here,
at the lexer level, as lexical errors.
"""

KEYWORDS = {"ls", "cd", "cat", "print", "exec"}


class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value!r})"

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value


class LexError(Exception):
    """Raised when the tokenizer encounters invalid input."""
    pass


def tokenize(line):
    """
    Convert a raw command-line string into a list of Token objects,
    ending with an EOF token.

    Raises LexError on malformed names or unexpected characters.
    """
    tokens = []
    i = 0
    n = len(line)

    while i < n:
        c = line[i]

        # --- whitespace: skip ---
        if c.isspace():
            i += 1
            continue

        # --- ROOT token: bare backslash ---
        if c == '\\':
            tokens.append(Token("ROOT", "\\"))
            i += 1
            continue

        # --- letters/digits: keyword, FILENAME, or FOLDERNAME ---
        # (Names may start with a letter and contain letters/digits,
        # matching classic DOS 8.3 naming, e.g. "REPORT1.TXT")
        if c.isalpha():
            start = i
            while i < n and line[i].isalnum():
                i += 1
            word = line[start:i]

            # Case: followed by a dot -> must be a FILENAME (8 chars . 3 chars)
            if i < n and line[i] == '.':
                i += 1  # consume the dot
                ext_start = i
                while i < n and line[i].isalnum():
                    i += 1
                ext = line[ext_start:i]

                # after the extension letters, the name must end
                # (i.e. next char must be whitespace or end of string)
                if i < n and not line[i].isspace():
                    raise LexError(
                        f"Malformed filename near position {start}: "
                        f"'{word}.{ext}{line[i]}...'"
                    )

                if len(word) == 8 and len(ext) == 3:
                    tokens.append(Token("FILENAME", f"{word}.{ext}"))
                else:
                    raise LexError(
                        f"Malformed filename '{word}.{ext}': "
                        f"expected 8 chars + '.' + 3 chars"
                    )
                continue

            # Case: no dot -> keyword or FOLDERNAME
            if word.lower() in KEYWORDS:
                tokens.append(Token(word.upper(), word))
            else:
                if 1 <= len(word) <= 8:
                    tokens.append(Token("FOLDERNAME", word))
                else:
                    raise LexError(
                        f"Malformed folder name '{word}': "
                        f"expected 1 to 8 chars"
                    )
            continue

        # --- anything else is invalid ---
        raise LexError(f"Unexpected character '{c}' at position {i}")

    tokens.append(Token("EOF", None))
    return tokens


# ---------------------------------------------------------------------------
# Manual test driver
# ---------------------------------------------------------------------------
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
    ]

    invalid_tests = [
        "cat TOOLONGNAME.TXT",    # name part too long (9 chars)
        "cat REPORT12.TOOLONG",   # extension too long
        "cat REPORT12.TX",        # extension too short
        "cd TOOLONGFOLDER",       # folder name too long (12 chars)
        "cat REPORT12TXT",        # missing dot for filename-shaped command
        "foo BAR",                # not a keyword, not handled by tokenizer
        "cat REPORT12.TXT#",      # junk after filename
    ]

    print("=== Valid commands ===")
    for cmd in valid_tests:
        print(f"{cmd!r:30} -> {tokenize(cmd)}")

    print("\n=== Invalid commands (expect LexError) ===")
    for cmd in invalid_tests:
        try:
            result = tokenize(cmd)
            print(f"{cmd!r:30} -> {result}  (WARNING: expected an error)")
        except LexError as e:
            print(f"{cmd!r:30} -> LexError: {e}")