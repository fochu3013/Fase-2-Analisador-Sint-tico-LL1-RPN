from typing import List, Dict, Any, Union
import json, os
from .lexer_io import Lexer
from .parser_ll1 import Parser
from .ast_nodes import ASTNode
from .tokens import Token
from .token_io import read_tokens_json

def lerTokens(texto: str) -> List[Token]:
    lx = Lexer(texto)
    return list(lx.tokens())

def lerTokensDeArquivoJSON(caminho: str) -> List[Token]:
    with open(caminho, "r", encoding="utf-8") as f:
        objs = json.load(f)
    return read_tokens_json(objs)

def construirGramatica() -> Dict[str, Any]:
    return {
        "nao_terminais": ["PROGRAM","LIST","STMT","EXPR","COND","BLOCK","IF_STMT","WHILE_STMT"],
        "terminais": ["NUM","MEM","LPAREN","RPAREN","OP","RELOP","RES","IF","WHILE","EOF"],
        "observacao": "FIRST/FOLLOW e Tabela LL(1) documentadas em docs/gramatica_ebnf.md"
    }

def parsear(tokens: List[Token]) -> ASTNode:
    p = Parser(tokens)
    return p.parse_program()

def gerarArvore(ast: ASTNode) -> Any:
    return ast.to_dict()
