from __future__ import annotations
import ply.yacc as yacc
import sys
from lex import tokens
from enum import Enum
from typing import Union

# expr : def_alphabet
#      | def_states
#      | def_rule
#      | comment

# comment : COMMENT

# def_alphabet : DEF_ALPH L_BR alp_symbols R_BR
#
# alp_symbols : alp_symbol
#             | alp_symbols SEPR alp_symbol
#
# alp_symbol : SYMBOL
#            | EMPTY_SYMBOL

# def_states : DEF_STATES L_BR set_states R_BR
#
# set_states : set_state
#            | set_states SEPR set_state
#
# set_state : STATE

# def_rule : left_part BIND right_part
# 
# left_part : L_BR state SEPR symbol R_BR
#
# right_part : L_BR opt_symbol SEPR opt_move_head SEPR opt_state R_BR
#
# state : STATE
#
# symbol : SYMBOL
#        | EMPTY_SYMBOL 
#
# opt_symbol : symbol
#            | NONE
#
# opt_move_head : MOVE_HEAD
#               | NONE
#
# opt_state : state
#           | NONE


class MoveHead(Enum):
    Left = 1
    Right = 2


class FinalState:
    def to_string(self):
        return "Final State"

    def __repr__(self):
        return "Final State"


class EmptySymbol:
    def to_string(self):
        return "_"

    def __repr__(self):
        return "_"


class RuleLeftPart:
    state: str
    symbol: Union[str, EmptySymbol]

    def __init__(self, state, symbol):
        self.state = state
        self.symbol = symbol

    def __str__(self):
        result = ""
        if isinstance(self.state, FinalState):
            result += "(" + self.state.to_string() + ", "
        else:
            result += "(" + str(self.state) + ", "
        
        if isinstance(self.symbol, EmptySymbol):
            result += self.symbol.to_string() + ")"
        else:
            result += str(self.symbol) + ")"
        return result

    def __key(self):
        return (self.state, self.symbol)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, RuleLeftPart):
            return self.__key() == other.__key()
        return NotImplemented


class RuleRightPart:
    new_symbol: Union[str, EmptySymbol, None]
    move_head: Union[MoveHead, None]
    new_state: Union[str, FinalState, None]

    def __init__(self, new_symbol, move_head, new_state):
        self.new_symbol = new_symbol
        self.move_head = move_head
        self.new_state = new_state

    def __str__(self):
        result = "("

        if isinstance(self.new_symbol, EmptySymbol):
            result += self.new_symbol.to_string() + ")"
        else:
            result += str(self.new_symbol) + ", "

        if self.move_head == MoveHead.Left:
            result += "Left, "
        elif self.move_head == MoveHead.Right:
            result += "Right, "
        else:
            result += "None, "
        
        if isinstance(self.new_state, FinalState):
            result += self.new_state.to_string() + ")"
        else:
            result += str(self.new_state) + ")"
        return result


class TuringMachine:
    alphabet = set()
    states: set[Union[str, FinalState]] = set()
    rules: dict[RuleLeftPart, RuleRightPart] = dict()

    def __str__(self):
        result = ""
        result += "Alphabet: " + str(self.alphabet) + "\n"
        result += "States: " + str(self.states) + "\n"
        result += "Rules: \n"
        for left_part in self.rules:
            result += "\t" + str(left_part) + " -> " + str(self.rules[left_part]) + "\n"
        return result

machine = TuringMachine()


def p_expr_alp(p):
    'expr : def_alphabet'
    p[0] = p[1]

def p_alphabet(p):
    'def_alphabet : DEF_ALPH L_BR alp_symbols R_BR'
    p[0] = p[3]

def p_alp_symbols_symbol(p):
    'alp_symbols : alp_symbol'
    p[0] = [p[1]]

def p_alp_symbols_symbols(p):
    'alp_symbols : alp_symbols SEPR alp_symbol'
    p[0] = p[1] + [p[3]]

def p_alp_symbol_empty(p):
    'alp_symbol : EMPTY_SYMBOL'
    p[0] = p[1]
    machine.alphabet.add(EmptySymbol())

def p_alp_symbol_symbol(p):
    'alp_symbol : SYMBOL'
    p[0] = p[1]
    machine.alphabet.add(p[0])


def p_expr_states(p):
    'expr : def_states'
    p[0] = p[1]


def p_def_states(p):
    'def_states : DEF_STATES L_BR set_states R_BR'
    p[0] = p[3]

def p_set_states_state(p):
    'set_states : set_state'
    p[0] = [p[1]]

def p_set_states_states(p):
    'set_states : set_states SEPR set_state'
    p[0] = p[1] + [p[3]]

def p_set_state(p):
    'set_state : STATE'
    p[0] = p[1]
    if p[0] == "!":
        machine.states.add(FinalState())
    else:
        machine.states.add(p[0])


def p_expr_rule(p):
    'expr : def_rule'
    p[0] = p[1]

def p_def_rule(p):
    'def_rule : left_part BIND right_part'
    p[0] = (p[1], p[3])
    if p[0][0] in machine.rules:
        print("UB: multiple definition for rule " + str(p[0][0]))
    else:
        machine.rules[p[0][0]] = p[0][1]

def p_left_part(p):
    'left_part : L_BR state SEPR symbol R_BR'
    p[0] = RuleLeftPart(p[2], p[4])
    if isinstance(p[0].state, FinalState):
        print("UB: Final State in left part of rule " + str(p[0]))

def p_right_part(p):
    'right_part : L_BR opt_symbol SEPR opt_move_head SEPR opt_state R_BR'
    p[0] = RuleRightPart(p[2], p[4], p[6])

def p_state(p):
    'state : STATE'
    if p[1] == "!":
        p[0] = FinalState()
    else:
        p[0] = p[1]

def p_symbol_symbol(p):
    'symbol : SYMBOL'
    p[0] = p[1]

def p_symbol_empty(p):
    'symbol : EMPTY_SYMBOL'
    p[0] = EmptySymbol()

def p_opt_symbol_symbol(p):
    'opt_symbol : symbol'
    p[0] = p[1]

def p_opt_symbol_none(p):
    'opt_symbol : NONE'
    p[0] = None

def p_opt_move_head_move_head(p):
    'opt_move_head : MOVE_HEAD'
    if p[1] == "L":
        p[0] = MoveHead.Left
    else:
        p[0] = MoveHead.Right

def p_opt_move_head_none(p):
    'opt_move_head : NONE'
    p[0] = None

def p_opt_state_state(p):
    'opt_state : state'
    p[0] = p[1]

def p_opt_state_none(p):
    'opt_state : NONE'
    p[0] = None

def p_error(p):
    if p is None:
        print("Unexpected end of input")
    else:
        t = f"{p.type}({p.value}) at {p.lineno}:{p.lexpos}"
        print(f"Syntax error: Unexpected {t}", p)
    

def p_expr_comment(p):
    'expr : comment'
    p[0] = p[1]

def p_comment_comment(p):
    'comment : COMMENT'
    p[0] = p[1]


def main():
    if len(sys.argv) > 1:
        filename = str(sys.argv[1])

        with open(filename, 'r') as fin, open(filename + ".out", "w") as fout:
            parser = yacc.yacc()
            for line in fin.readlines():
                parser.parse(line)

            print(str(machine), file=fout, end='')


if __name__ == "__main__":
    main()