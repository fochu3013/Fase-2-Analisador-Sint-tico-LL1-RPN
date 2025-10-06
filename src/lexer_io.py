import re
from .tokens import Token, TokenType

RE_WS  = re.compile(r"\s+")
RE_NUM = re.compile(r"\d+(?:\.\d+)?\b")
RE_MEM = re.compile(r"[A-Z]+\b")  # memórias em maiúsculas
RE_ID  = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\b")

OPS = {"+", "-", "*", "|", "/", "%", "^"}
RELOPS = {">=", "<=", "==", "!=", ">", "<"}

KEYWORDS = {
    "RES": TokenType.RES,
    "IF": TokenType.IF,
    "WHILE": TokenType.WHILE,
}

class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.i = 0
        self.line = 1
        self.col = 1

    def _advance(self, n: int):
        for _ in range(n):
            if self.text[self.i] == "\n":
                self.line += 1
                self.col = 1
            else:
                self.col += 1
            self.i += 1

    def _emit(self, type_, lexeme):
        return Token(type_, lexeme, self.line, self.col)

    def tokens(self):
        text = self.text
        n = len(text)
        while self.i < n:
            m = RE_WS.match(text, self.i)
            if m:
                self._advance(m.end() - self.i)
                if self.i >= n:
                    break
            if self.i >= n:
                break

            ch = text[self.i]

            if ch == '(':
                tok = self._emit(TokenType.LPAREN, ch)
                self._advance(1); yield tok; continue
            if ch == ')':
                tok = self._emit(TokenType.RPAREN, ch)
                self._advance(1); yield tok; continue
            
                

            # Relops: dois caracteres primeiro
            if self.i + 1 < n and text[self.i:self.i+2] in RELOPS:
                two = text[self.i:self.i+2]
                tok = self._emit(TokenType.RELOP, two)
                self._advance(2); yield tok; continue
            
            # Relops 1 char (>, <)  -------------------------------------------------
            if ch in {">", "<"}:
                tok = Token(TokenType.RELOP, ch, self.line, self.col)
                self._advance(1)
                yield tok
                continue

            # Ops 1 char (inclui '|')
            if ch in OPS:
                tok = self._emit(TokenType.OP, ch)
                self._advance(1); yield tok; continue

            # NUM
            m = RE_NUM.match(text, self.i)
            if m:
                lex = m.group(0)
                tok = self._emit(TokenType.NUM, lex)
                self._advance(len(lex)); yield tok; continue

            # MEM (maiúsculas) tem prioridade sobre KEYWORDS
            m = RE_MEM.match(text, self.i)
            if m:
                lex = m.group(0)
                # Palavras-chave?
                ttype = KEYWORDS.get(lex, TokenType.MEM)
                tok = self._emit(ttype, lex)
                self._advance(len(lex)); yield tok; continue

            # ID genérico (não usado diretamente aqui, mas preservado)
            m = RE_ID.match(text, self.i)
            if m:
                lex = m.group(0)
                ttype = KEYWORDS.get(lex, TokenType.ID)
                tok = self._emit(ttype, lex)
                self._advance(len(lex)); yield tok; continue

            raise SyntaxError(f"Caractere inválido '{ch}' em {self.line}:{self.col}")

        yield Token(TokenType.EOF, "<EOF>", self.line, self.col)
