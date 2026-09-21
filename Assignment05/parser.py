"""
Caleb Morris
Assignment05

Step 3: Hand-built recursive descent parser.

Updated EBNF Grammar:

    program      ::= command

    command      ::= ls_cmd
                   | cd_cmd
                   | cat_cmd
                   | print_cmd
                   | exec_cmd
                   | set_cmd
                   | echo_cmd

    ls_cmd       ::= "ls" [ argument ]

    cd_cmd       ::= "cd" [ argument | ROOT ]

    cat_cmd      ::= "cat" argument

    print_cmd    ::= "print" argument

    exec_cmd     ::= "exec" argument

    set_cmd      ::= "SET" VARIABLE "=" expression

    echo_cmd     ::= "echo" VARIABLE

    argument     ::= FILENAME
                   | FOLDERNAME
                   | VARIABLE

    expression   ::= term { ("+" | "-") term }

    term         ::= factor { ("*" | "/") factor }

    factor       ::= VARIABLE
                   | STRING
                   | "(" expression ")"

    VARIABLE     ::= "$" IDENTIFIER

    IDENTIFIER   ::= LETTER { LETTER | DIGIT }

    LETTER       ::= "A" | "B" | ... | "Z"
                   | "a" | "b" | ... | "z"

    DIGIT        ::= "0" | "1" | ... | "9"

    ROOT         ::= "\\"

Start symbol:
    program

Updated variables:
    VARIABLE
    IDENTIFIER
    LETTER
    DIGIT

Updated tokens:
    LS
    CD
    CAT
    PRINT
    EXEC
    SET
    ECHO
    FILENAME
    FOLDERNAME
    VARIABLE
    ROOT
    EQUALS
    PLUS
    MINUS
    MULTIPLY
    DIVIDE
    LEFT_PAREN
    RIGHT_PAREN
    EOF

The parser does not evaluate arithmetic expressions.
Expressions are only parsed and represented in the AST.
"""

from tokenizer import tokenize, LexError


class ParseError(Exception):
    """Raised when the token stream does not match the grammar."""
    pass


# ===================================================================
# AST NODE DEFINITIONS
# ===================================================================

class ASTNode:
    def __repr__(self):
        return self._repr()


class Command(ASTNode):
    def __init__(self, sub_cmd):
        self.sub_cmd = sub_cmd

    def _repr(self):
        return f"Command({self.sub_cmd!r})"


class LsCmd(ASTNode):
    def __init__(self, arg=None):
        self.arg = arg

    def _repr(self):
        return f"LsCmd(arg={self.arg!r})"


class CdCmd(ASTNode):
    def __init__(self, arg=None):
        self.arg = arg

    def _repr(self):
        return f"CdCmd(arg={self.arg!r})"


class CatCmd(ASTNode):
    def __init__(self, argument):
        self.argument = argument

    def _repr(self):
        return f"CatCmd(argument={self.argument!r})"


class PrintCmd(ASTNode):
    def __init__(self, argument):
        self.argument = argument

    def _repr(self):
        return f"PrintCmd(argument={self.argument!r})"


class ExecCmd(ASTNode):
    def __init__(self, argument):
        self.argument = argument

    def _repr(self):
        return f"ExecCmd(argument={self.argument!r})"


class Variable(ASTNode):
    def __init__(self, name):
        self.name = name

    def _repr(self):
        return f"Variable({self.name!r})"


class String(ASTNode):
    def __init__(self, value):
        self.value = value

    def _repr(self):
        return f"String({self.value!r})"


class SetCmd(ASTNode):
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression

    def _repr(self):
        return (
            f"SetCmd(variable={self.variable!r}, "
            f"expression={self.expression!r})"
        )


class EchoCmd(ASTNode):
    def __init__(self, variable):
        self.variable = variable

    def _repr(self):
        return f"EchoCmd(variable={self.variable!r})"


class BinaryExpression(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def _repr(self):
        return (
            f"BinaryExpression("
            f"left={self.left!r}, "
            f"operator={self.operator!r}, "
            f"right={self.right!r})"
        )


# ===================================================================
# PARSER
# ===================================================================

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

        # Symbol table:
        # variable name -> current string value
        self.symbol_table = {}

    # ---------------------------------------------------------------
    # Token helpers
    # ---------------------------------------------------------------

    def current(self):
        return self.tokens[self.pos]

    def advance(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect(self, type_):
        tok = self.current()

        if tok.type != type_:
            raise ParseError(
                f"Expected {type_}, "
                f"got {tok.type} ({tok.value!r})"
            )

        return self.advance()

    # ---------------------------------------------------------------
    # program ::= command
    # ---------------------------------------------------------------

    def parse_program(self):
        node = self.parse_command()

        self.expect("EOF")

        return node

    # ---------------------------------------------------------------
    # command
    # ---------------------------------------------------------------

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

        elif tok.type == "SET":
            node = self.parse_set_cmd()

        elif tok.type == "ECHO":
            node = self.parse_echo_cmd()

        else:
            raise ParseError(
                f"Unrecognized command: "
                f"{tok.type} ({tok.value!r})"
            )

        return Command(node)

    # ---------------------------------------------------------------
    # ls_cmd ::= "ls" [ argument ]
    # ---------------------------------------------------------------

    def parse_ls_cmd(self):
        self.expect("LS")

        tok = self.current()

        if tok.type in (
            "FILENAME",
            "FOLDERNAME",
            "VARIABLE"
        ):
            self.advance()
            return LsCmd(arg=tok.value)

        return LsCmd(arg=None)

    # ---------------------------------------------------------------
    # cd_cmd ::= "cd" [ argument | ROOT ]
    # ---------------------------------------------------------------

    def parse_cd_cmd(self):
        self.expect("CD")

        tok = self.current()

        if tok.type in (
            "FOLDERNAME",
            "VARIABLE",
            "ROOT"
        ):
            self.advance()
            return CdCmd(arg=tok.value)

        return CdCmd(arg=None)

    # ---------------------------------------------------------------
    # cat_cmd ::= "cat" argument
    # ---------------------------------------------------------------

    def parse_cat_cmd(self):
        self.expect("CAT")

        tok = self.current()

        if tok.type not in (
            "FILENAME",
            "FOLDERNAME",
            "VARIABLE"
        ):
            raise ParseError(
                "Expected FILENAME, FOLDERNAME, or VARIABLE "
                f"but got {tok.type}"
            )

        self.advance()

        return CatCmd(argument=tok.value)

    # ---------------------------------------------------------------
    # print_cmd ::= "print" argument
    # ---------------------------------------------------------------

    def parse_print_cmd(self):
        self.expect("PRINT")

        tok = self.current()

        if tok.type not in (
            "FILENAME",
            "FOLDERNAME",
            "VARIABLE"
        ):
            raise ParseError(
                "Expected FILENAME, FOLDERNAME, or VARIABLE "
                f"but got {tok.type}"
            )

        self.advance()

        return PrintCmd(argument=tok.value)

    # ---------------------------------------------------------------
    # exec_cmd ::= "exec" argument
    # ---------------------------------------------------------------

    def parse_exec_cmd(self):
        self.expect("EXEC")

        tok = self.current()

        if tok.type not in (
            "FILENAME",
            "FOLDERNAME",
            "VARIABLE"
        ):
            raise ParseError(
                "Expected FILENAME, FOLDERNAME, or VARIABLE "
                f"but got {tok.type}"
            )

        self.advance()

        return ExecCmd(argument=tok.value)

    # ---------------------------------------------------------------
    # set_cmd ::= "SET" VARIABLE "=" expression
    # ---------------------------------------------------------------

    def parse_set_cmd(self):
        self.expect("SET")

        variable_token = self.expect("VARIABLE")

        self.expect("EQUALS")

        expression = self.parse_expression()

        # Store the expression's string representation in the
        # symbol table because this assignment only parses.
        self.symbol_table[variable_token.value] = str(expression)

        return SetCmd(
            Variable(variable_token.value),
            expression
        )

    # ---------------------------------------------------------------
    # echo_cmd ::= "echo" VARIABLE
    # ---------------------------------------------------------------

    def parse_echo_cmd(self):
        self.expect("ECHO")

        variable_token = self.expect("VARIABLE")

        # Variables are defined upon first use.
        if variable_token.value not in self.symbol_table:
            self.symbol_table[variable_token.value] = ""

        return EchoCmd(
            Variable(variable_token.value)
        )

    # ---------------------------------------------------------------
    # expression ::= term { ("+" | "-") term }
    # ---------------------------------------------------------------

    def parse_expression(self):
        left = self.parse_term()

        while self.current().type in ("PLUS", "MINUS"):

            operator = self.advance()

            right = self.parse_term()

            left = BinaryExpression(
                left,
                operator.value,
                right
            )

        return left

    # ---------------------------------------------------------------
    # term ::= factor { ("*" | "/") factor }
    # ---------------------------------------------------------------

    def parse_term(self):
        left = self.parse_factor()

        while self.current().type in (
            "MULTIPLY",
            "DIVIDE"
        ):

            operator = self.advance()

            right = self.parse_factor()

            left = BinaryExpression(
                left,
                operator.value,
                right
            )

        return left

    # ---------------------------------------------------------------
    # factor ::= VARIABLE | STRING | "(" expression ")"
    # ---------------------------------------------------------------

    def parse_factor(self):

        tok = self.current()

        # VARIABLE
        if tok.type == "VARIABLE":

            self.advance()

            # Variables are defined upon first use.
            if tok.value not in self.symbol_table:
                self.symbol_table[tok.value] = ""

            return Variable(tok.value)

        # STRING
        #
        # In this assignment, the tokenizer's FOLDERNAME and FILENAME
        # values are treated as strings for expression parsing.
        if tok.type in (
            "FOLDERNAME",
            "FILENAME"
        ):

            self.advance()

            return String(tok.value)

        # Parenthesized expression
        if tok.type == "LEFT_PAREN":

            self.advance()

            expression = self.parse_expression()

            self.expect("RIGHT_PAREN")

            return expression

        raise ParseError(
            f"Expected VARIABLE, STRING, or '(' "
            f"but got {tok.type} ({tok.value!r})"
        )


# ===================================================================
# PARSE FUNCTION
# ===================================================================

def parse(line):
    """
    Tokenize and parse a raw command.

    Returns:
        Command AST

    Prints:
        Symbol table after a successful parse.
    """

    tokens = tokenize(line)

    parser = Parser(tokens)

    tree = parser.parse_program()

    print("Symbol Table:")
    if parser.symbol_table:
        for name, value in parser.symbol_table.items():
            print(f"  {name} = {value}")
    else:
        print("  {}")

    return tree


# ===================================================================
# MANUAL TEST DRIVER
# ===================================================================

if __name__ == "__main__":

    valid_tests = [
        # Original commands
        "ls",
        "ls MYDOCS",
        "cd",
        "cd MYDOCS",
        "cd \\",
        "cat REPORT12.TXT",
        "print REPORT12.TXT",
        "exec PROGRAM1.EXE",

        # Variables
        "echo $x",
        "SET $x = hello",
        "SET $name = Caleb",

        # Expressions
        "SET $x = $y",
        "SET $x = $y + $z",
        "SET $x = $a * $b",
        "SET $x = $a + $b * $c",
        "SET $x = ($a + $b) * $c",

        # Variables used by other commands
        "ls $x",
        "cd $x",
        "cat $x",
        "print $x",
        "exec $x",
    ]

    invalid_tests = [
        "cat",
        "cat MYDOCS EXTRA",
        "SET",
        "SET $x",
        "SET $x =",
        "SET = hello",
        "echo",
        "echo hello",
        "SET $123 = hello",
        "SET $x = $a +",
        "SET $x = ($a + $b",
    ]

    print("========================================")
    print("VALID TESTS")
    print("========================================")

    for command in valid_tests:

        print(f"\nInput: {command}")

        try:
            result = parse(command)
            print(f"AST: {result}")

        except (ParseError, LexError) as e:
            print(
                f"ERROR: {type(e).__name__}: {e}"
            )

    print("\n========================================")
    print("INVALID TESTS")
    print("========================================")

    for command in invalid_tests:

        print(f"\nInput: {command}")

        try:
            result = parse(command)

            print(
                f"WARNING: expected an error, "
                f"but got {result}"
            )

        except (ParseError, LexError) as e:
            print(
                f"{type(e).__name__}: {e}"
            )