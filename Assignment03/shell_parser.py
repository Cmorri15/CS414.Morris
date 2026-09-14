"""
Caleb Morris
Assignment03
This is step three of this assignment. I did have the help of Claude.ai when completing this assingment.

Step 3: Hand-built recursive descent parser for the simple shell command set.

EBNF Grammar :
    command    ::= ls_cmd | cd_cmd | cat_cmd | print_cmd | exec_cmd
    ls_cmd     ::= "ls" [ FILENAME | FOLDERNAME ]
    cd_cmd     ::= "cd" [ FOLDERNAME | ROOT ]
    cat_cmd    ::= "cat" FILENAME
    print_cmd  ::= "print" FILENAME
    exec_cmd   ::= "exec" FILENAME

    FILENAME   ::= 8 chars "." 3 chars
    FOLDERNAME ::= 1 to 8 chars (no dot)
    ROOT       ::= "\"

Tokens: LS, CD, CAT, PRINT, EXEC, FILENAME, FOLDERNAME, ROOT, EOF

Takes the token list produced by tokenizer.py and either returns an AST
node for the command, or raises ParseError if the syntax is invalid.
"""

from tokenizer import tokenize, LexError


class ParseError(Exception):
    """Raised when the token stream does not match the grammar."""
    pass


# ---------------------------------------------------------------------------
# AST node definitions
# ---------------------------------------------------------------------------
class ASTNode:
    def __repr__(self):
        return self._repr()


class Command(ASTNode):
    """Top-level node: wraps whichever specific command was parsed."""
    def __init__(self, sub_cmd):
        self.sub_cmd = sub_cmd

    def _repr(self):
        return f"Command({self.sub_cmd!r})"


class LsCmd(ASTNode):
    def __init__(self, arg=None):
        self.arg = arg  # None, or a name string

    def _repr(self):
        return f"LsCmd(arg={self.arg!r})"


class CdCmd(ASTNode):
    def __init__(self, arg=None):
        self.arg = arg  # None, "\\" for root, or a folder name string

    def _repr(self):
        return f"CdCmd(arg={self.arg!r})"


class CatCmd(ASTNode):
    def __init__(self, filename):
        self.filename = filename

    def _repr(self):
        return f"CatCmd(filename={self.filename!r})"


class PrintCmd(ASTNode):
    def __init__(self, filename):
        self.filename = filename

    def _repr(self):
        return f"PrintCmd(filename={self.filename!r})"


class ExecCmd(ASTNode):
    def __init__(self, filename):
        self.filename = filename

    def _repr(self):
        return f"ExecCmd(filename={self.filename!r})"


# ---------------------------------------------------------------------------
# Recursive descent parser
# ---------------------------------------------------------------------------
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos]

    def advance(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect(self, type_):
        tok = self.current()
        if tok.type != type_:
            raise ParseError(f"Expected {type_}, got {tok.type} ({tok.value!r})")
        return self.advance()

    # command ::= ls_cmd | cd_cmd | cat_cmd | print_cmd | exec_cmd
    def parse_command(self):
        tok = self.current()

        if tok.type == "LS":
            node = self.parse_ls_cmd()
        elif tok.type == "CD":
            node = self.parse_cd_cmd()
        elif tok.type == "CAT":
            node = self.parse_cat_cmd()
        elif tok.type == "PRINT":
            node = self.parse_print_cmd()
        elif tok.type == "EXEC":
            node = self.parse_exec_cmd()
        else:
            raise ParseError(f"Unrecognized command: {tok.type} ({tok.value!r})")

        self.expect("EOF")  # ensure no trailing garbage
        return Command(node)

    # ls_cmd ::= "ls" [ FILENAME | FOLDERNAME ]
    def parse_ls_cmd(self):
        self.expect("LS")
        tok = self.current()
        if tok.type in ("FILENAME", "FOLDERNAME"):
            self.advance()
            return LsCmd(arg=tok.value)
        return LsCmd(arg=None)

    # cd_cmd ::= "cd" [ FOLDERNAME | ROOT ]
    def parse_cd_cmd(self):
        self.expect("CD")
        tok = self.current()
        if tok.type in ("FOLDERNAME", "ROOT"):
            self.advance()
            return CdCmd(arg=tok.value)
        return CdCmd(arg=None)

    # cat_cmd ::= "cat" FILENAME
    def parse_cat_cmd(self):
        self.expect("CAT")
        tok = self.expect("FILENAME")
        return CatCmd(filename=tok.value)

    # print_cmd ::= "print" FILENAME
    def parse_print_cmd(self):
        self.expect("PRINT")
        tok = self.expect("FILENAME")
        return PrintCmd(filename=tok.value)

    # exec_cmd ::= "exec" FILENAME
    def parse_exec_cmd(self):
        self.expect("EXEC")
        tok = self.expect("FILENAME")
        return ExecCmd(filename=tok.value)


def parse(line):
    """Tokenize and parse a raw command string. Returns an AST (Command)."""
    tokens = tokenize(line)
    parser = Parser(tokens)
    return parser.parse_command()


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
        "cat",                      # missing required FILENAME
        "cat MYDOCS",                # FOLDERNAME where FILENAME required
        "cd REPORT12.TXT",           # FILENAME where FOLDERNAME/ROOT required
        "cat REPORT12.TXT extra",    # trailing garbage
        "foo BAR",                   # not a recognized command
        "cat TOOLONGNAME.TXT",       # lexer-level error, bubbles up
    ]

    print("=== Valid commands ===")
    for cmd in valid_tests:
        print(f"{cmd!r:25} -> {parse(cmd)}")

    print("\n=== Invalid commands (expect errors) ===")
    for cmd in invalid_tests:
        try:
            result = parse(cmd)
            print(f"{cmd!r:25} -> {result}  (WARNING: expected an error)")
        except (ParseError, LexError) as e:
            print(f"{cmd!r:25} -> {type(e).__name__}: {e}")