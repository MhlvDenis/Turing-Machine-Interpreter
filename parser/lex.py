import ply.lex as lex
import sys

tokens = [
    "BIND",
    "L_BR",
    "R_BR",
    "NONE",
    "SEPR",
    "SYMBOL",
    "STATE", 
    "DEF_ALPH",
    "DEF_STATES",
    "EMPTY_SYMBOL",
    "MOVE_HEAD",
    "COMMENT"
]

t_BIND = r'->'
t_L_BR = r'\('
t_R_BR = r'\)'
t_NONE = r'None'
t_SEPR = r','
t_DEF_ALPH = r'Alphabet'
t_DEF_STATES = r'States'
t_EMPTY_SYMBOL = r'_'
t_MOVE_HEAD = r'(L|R)'

t_ignore = ' \t'


def t_SYMBOL(t):
    r'\'.\''
    t.value = t.value[1:-1]
    return t


def t_STATE(t):
    r'\$(\!|[0-9]+)'
    t.value = t.value[1:]
    return t


def t_COMMENT(t):
    r'\#.*'
    t.value = t.value[1:]
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()


def main():
    if len(sys.argv) > 1:
        filename = str(sys.argv[1])

        with open(filename, 'r') as fin, open(filename + ".out", "w") as fout:
            lexer.input("".join(fin.readlines()))

            while True:
                tok = lexer.token()
                if not tok:
                    break
                print(tok, file=fout)


if __name__ == "__main__":
    main()
