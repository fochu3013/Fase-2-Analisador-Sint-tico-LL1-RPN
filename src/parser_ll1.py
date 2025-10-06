from typing import List, Optional
from .tokens import Token, TokenType
from .errors import ParseError
from . import ast_nodes as AST

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.i = 0

    def peek(self) -> Token:
        return self.tokens[self.i]

    def advance(self) -> Token:
        t = self.tokens[self.i]
        self.i += 1
        return t

    def expect(self, ttype: TokenType, msg: str):
        t = self.peek()
        if t.type != ttype:
            raise ParseError(f"{msg}. Encontrado: {t.type.name} '{t.lexeme}'", t.line, t.col)
        return self.advance()

    # Wrappers LL(1)-style
    def parse_program(self) -> AST.ASTNode:
        lst = self.parse_list()
        self.expect(TokenType.EOF, "EOF esperado ao final do programa")
        return AST.program(lst)

    # LIST → STMT LIST | ε
    def parse_list(self) -> AST.ASTNode:
        stmts = []
        while True:
            la = self.peek().type
            if la in (TokenType.NUM, TokenType.LPAREN, TokenType.MEM):
                stmts.append(self.parse_stmt())
            else:
                break
        return AST.block(stmts)

    # STMT → EXPR | IF_STMT | WHILE_STMT
    def parse_stmt(self) -> AST.ASTNode:
        if self.peek().type == TokenType.LPAREN:
            # tentativas ordenadas: IF, WHILE, senão EXPR
            save = self.i
            try:
                return self.parse_if_stmt()
            except ParseError:
                self.i = save
            save = self.i
            try:
                return self.parse_while_stmt()
            except ParseError:
                self.i = save
            return self.parse_expr()
        elif self.peek().type in (TokenType.NUM, TokenType.MEM):
            return self.parse_expr()
        else:
            t = self.peek()
            raise ParseError("Início de sentença inválido", t.line, t.col)

    # EXPR
    # → NUM
    # | MEMLOAD              # (MEM)
    # | RESCMD               # (N RES)
    # | MEMSTORE             # (V MEM)
    # | '(' EXPR EXPR OP ')'
    # | '(' EXPR RES ')'     # opcional (print unário)
    def parse_expr(self) -> AST.ASTNode:
        la = self.peek().type
        if la == TokenType.NUM:
            return AST.num(self.advance().lexeme)
        if la == TokenType.MEM:
            # Forma MEMLOAD tratada apenas como literal MEM isolado? Não.
            # MEMLOAD deve estar entre parênteses, então aqui é só erro se MEM solto.
            t = self.peek()
            raise ParseError("MEM deve ser usado como (MEM) ou (V MEM)", t.line, t.col)

        if la == TokenType.LPAREN:
            self.advance()
            # Tentar ( NUM RES )
            save = self.i
            try:
                n = self.expect(TokenType.NUM, "Número esperado em (N RES)")
                self.expect(TokenType.RES, "RES esperado em (N RES)")
                self.expect(TokenType.RPAREN, "')' esperado")
                return AST.rescmd(AST.num(n.lexeme))
            except ParseError:
                self.i = save

            # Tentar ( NUM MEM )  -> MEMSTORE
            save = self.i
            try:
                v = self.expect(TokenType.NUM, "Número esperado em (V MEM)")
                m = self.expect(TokenType.MEM, "MEM esperado (maiúsculas)")
                self.expect(TokenType.RPAREN, "')' esperado")
                return AST.memstore(AST.num(v.lexeme), AST.mem(m.lexeme))
            except ParseError:
                self.i = save

            # Tentar ( MEM ) -> MEMLOAD
            save = self.i
            try:
                m = self.expect(TokenType.MEM, "MEM esperado em (MEM)")
                self.expect(TokenType.RPAREN, "')' esperado")
                return AST.memload(AST.mem(m.lexeme))
            except ParseError:
                self.i = save

            # Tentar '(' EXPR EXPR RELOP ')' -> não é EXPR; é COND, mas pode aparecer dentro de IF/WHILE
            # então não consumimos aqui.

            # Tentar '(' EXPR EXPR OP ')'
            save = self.i
            try:
                e1 = self.parse_expr()
                e2 = self.parse_expr()
                op = self.expect(TokenType.OP, "Operador aritmético esperado (+ - * | / % ^)")
                self.expect(TokenType.RPAREN, "')' esperado")
                return AST.binop(op.lexeme, e1, e2)
            except ParseError:
                self.i = save

            # Tentar '(' EXPR RES ')' (print)
            save = self.i
            try:
                e = self.parse_expr()
                self.expect(TokenType.RES, "RES esperado ao final de '( EXPR RES )'")
                self.expect(TokenType.RPAREN, "')' esperado")
                return AST.res(e)
            except ParseError:
                self.i = save

            t = self.peek()
            raise ParseError("Forma de expressão inválida após '('", t.line, t.col)

        t = self.peek()
        raise ParseError(f"Expressão inválida: '{t.lexeme}'", t.line, t.col)

    # COND → '(' EXPR EXPR RELOP ')'
    def parse_cond(self) -> AST.ASTNode:
        self.expect(TokenType.LPAREN, "'(' esperado no início da condição")
        e1 = self.parse_expr()
        e2 = self.parse_expr()
        rel = self.expect(TokenType.RELOP, "Operador relacional esperado")
        self.expect(TokenType.RPAREN, "')' esperado na condição")
        return AST.relop(rel.lexeme, e1, e2)

    # BLOCK → '(' LIST ')'
    def parse_block(self) -> AST.ASTNode:
        self.expect(TokenType.LPAREN, "'(' esperado no início do bloco")
        lst = self.parse_list()
        self.expect(TokenType.RPAREN, "')' esperado no final do bloco")
        return AST.block(lst.children)

    # IF_STMT → '(' COND BLOCK BLOCK IF ')'
    def parse_if_stmt(self) -> AST.ASTNode:
        self.expect(TokenType.LPAREN, "'(' esperado no início do IF")
        cond = self.parse_cond()
        thenb = self.parse_block()
        elseb = self.parse_block()
        self.expect(TokenType.IF, "IF esperado antes de ')'")
        self.expect(TokenType.RPAREN, "')' esperado ao final do IF")
        return AST.ifnode(cond, thenb, elseb)

    # WHILE_STMT → '(' COND BLOCK WHILE ')'
    def parse_while_stmt(self) -> AST.ASTNode:
        self.expect(TokenType.LPAREN, "'(' esperado no início do WHILE")
        cond = self.parse_cond()
        body = self.parse_block()
        self.expect(TokenType.WHILE, "WHILE esperado antes de ')'")
        self.expect(TokenType.RPAREN, "')' esperado ao final do WHILE")
        return AST.whilenode(cond, body)
