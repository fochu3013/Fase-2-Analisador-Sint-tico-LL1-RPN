from typing import List, Dict, Any
from .tokens import Token, TokenType



_VARIANTS = {
    
    "LPAREN": TokenType.LPAREN, "L_PAREN": TokenType.LPAREN, "OPEN_PAREN": TokenType.LPAREN,
    "RPAREN": TokenType.RPAREN, "R_PAREN": TokenType.RPAREN, "CLOSE_PAREN": TokenType.RPAREN,

    "NUM": TokenType.NUM, "NUMBER": TokenType.NUM, "REAL": TokenType.NUM, "INT": TokenType.NUM,
    "ID": TokenType.ID, "IDENT": TokenType.ID, "IDENTIFIER": TokenType.ID,
    "MEM": TokenType.MEM,

    
    "OP": TokenType.OP,
    "PLUS": TokenType.OP, "MINUS": TokenType.OP, "TIMES": TokenType.OP, "MULT": TokenType.OP,
    "DIV": TokenType.OP, "DIVI": TokenType.OP, "DIVINT": TokenType.OP, "DIV_INT": TokenType.OP,
    "DIVR": TokenType.OP, "DIVREAL": TokenType.OP, "DIV_REAL": TokenType.OP,
    "MOD": TokenType.OP, "POW": TokenType.OP, "EXP": TokenType.OP,
    

    # Relops
    "RELOP": TokenType.RELOP,
    "GT": TokenType.RELOP, "LT": TokenType.RELOP, "GE": TokenType.RELOP, "LE": TokenType.RELOP,
    "EQ": TokenType.RELOP, "NE": TokenType.RELOP,

    # Keywords
    "RES": TokenType.RES,
    "IF": TokenType.IF,
    "WHILE": TokenType.WHILE,

    # EOF
    "EOF": TokenType.EOF
}

def _normalize_op_lexeme(t: Dict[str, Any]) -> str:
    
    lex = (t.get("lexeme") or "").strip()
    ttype = (t.get("type") or "").upper()

    by_type = {
        "PLUS": "+", "MINUS": "-", "TIMES": "*", "MULT": "*",
        "DIV": "/", "DIVI": "/", "DIVINT": "/", "DIV_INT": "/",
        "DIVR": "|", "DIVREAL": "|", "DIV_REAL": "|",
        "MOD": "%", "POW": "^", "EXP": "^"
    }
    if ttype in by_type:
        return by_type[ttype]

    by_lex = {"+": "+", "-": "-", "*": "*", "/": "/", "|": "|", "%": "%", "^": "^"}
    return by_lex.get(lex, lex or "+")

def _normalize_relop_lexeme(t: Dict[str, Any]) -> str:
    lex = (t.get("lexeme") or "").strip()
    ttype = (t.get("type") or "").upper()
    by_type = {
        "GT": ">", "LT": "<", "GE": ">=", "LE": "<=",
        "EQ": "==", "NE": "!="
    }
    if ttype in by_type:
        return by_type[ttype]
    by_lex = {">": ">", "<": "<", ">=": ">=", "<=": "<=", "==": "==", "!=": "!="}
    return by_lex.get(lex, lex or "==")

def _coerce_mem_if_upper_id(t: Dict[str, Any]) -> TokenType:
    
    if str(t.get("type","")).upper() in ("ID","IDENT","IDENTIFIER") and str(t.get("lexeme","")).isupper():
        return TokenType.MEM
    return _VARIANTS.get(str(t.get("type","")).upper(), TokenType.ID)

def read_tokens_json(objs: List[Dict[str, Any]]) -> List[Token]:
    out: List[Token] = []
    for t in objs:
       
        raw_type = str(t.get("type","")).upper()
        if raw_type == "OP" or raw_type in ("PLUS","MINUS","TIMES","MULT","DIV","DIVI","DIVINT","DIV_INT","DIVR","DIVREAL","DIV_REAL","MOD","POW","EXP"):
            ttype = TokenType.OP
            lex = _normalize_op_lexeme(t)
        elif raw_type == "RELOP" or raw_type in ("GT","LT","GE","LE","EQ","NE"):
            ttype = TokenType.RELOP
            lex = _normalize_relop_lexeme(t)
        elif raw_type in _VARIANTS:
            ttype = _VARIANTS[raw_type]
            lex = t.get("lexeme","")
        else:
           
            ttype = _coerce_mem_if_upper_id(t)
            lex = t.get("lexeme","")

        line = int(t.get("line") or 1)
        col = int(t.get("col") or 1)

        out.append(Token(ttype, lex, line, col))
   
    if not out or out[-1].type != TokenType.EOF:
        last = out[-1] if out else Token(TokenType.EOF,"<EOF>",1,1)
        out.append(Token(TokenType.EOF, "<EOF>", last.line, last.col))
    return out
