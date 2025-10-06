from dataclasses import dataclass
from enum import Enum, auto

class TokenType(Enum):
    LPAREN = auto()
    RPAREN = auto()
    NUM = auto()
    MEM = auto()       # memórias em MAIÚSCULAS
    ID = auto()
    OP = auto()        # + - * | / % ^
    RELOP = auto()     # > < >= <= == !=
    RES = auto()
    IF = auto()
    WHILE = auto()
    EOF = auto()

@dataclass
class Token:
    type: TokenType
    lexeme: str
    line: int
    col: int

    def __repr__(self):
        return f"Token({self.type.name}, '{self.lexeme}', {self.line}:{self.col})"
