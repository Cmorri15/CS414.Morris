## Caleb Morris
## Assignment03
## This is the step one of this assignment. I did have the help of Claude.ai when completing this assingment.

# EBNF Grammar
command    ::= ls_cmd | cd_cmd | cat_cmd | print_cmd | exec_cmd

ls_cmd     ::= "ls" [ FILENAME | FOLDERNAME ]
cd_cmd     ::= "cd" [ FOLDERNAME | ROOT ]
cat_cmd    ::= "cat" FILENAME
print_cmd  ::= "print" FILENAME
exec_cmd   ::= "exec" FILENAME

FILENAME   ::= LETTER LETTER LETTER LETTER LETTER LETTER LETTER LETTER "." LETTER LETTER LETTER
FOLDERNAME ::= LETTER {LETTER}
ROOT       ::= "\"
LETTER     ::= "A" | ... | "Z" | "a" | ... | "z"

# Tokens, Variables, Start Symbol
Tokens: LS, CD, CAT, PRINT, EXEC, FILENAME, FOLDERNAME, ROOT, EOF
Variables: command, ls_cmd, cd_cmd, cat_cmd, print_cmd, exec_cmd
Start symbol: command

# Examples and ASTs
ls - Lists the contents of the current folder (no argument).

AST:

      Command
         |
       LsCmd
         |
       (none)

ls MYDOCS - Lists the contents of a specified folder.

AST:

        Command
           |
         LsCmd
           |
      FolderName("MYDOCS")

cd - Changes current folder to root (no argument).

AST:

      Command
         |
       CdCmd
         |
       (none)

cd MYDOCS - Changes current folder to MYDOCS.

AST:

        Command
           |
         CdCmd
           |
      FolderName("MYDOCS")

cat REPORT1.TXT - Dumps a file to the display.

AST:

        Command
           |
        CatCmd
           |
     FileName("REPORT1.TXT")

print REPORT1.TXT - Prints a file to the attached printer.

AST:

         Command
            |
        PrintCmd
            |
     FileName("REPORT1.TXT")

exec PROGRAM1.EXE - Executes the named file.

AST:

        Command
            |
        ExecCmd
            |
     FileName("PROGRAM1.EXE")