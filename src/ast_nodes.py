from dataclasses import dataclass, field
from typing import Any, List, Dict

@dataclass
class ASTNode:
    kind: str
    value: Any = None
    children: List['ASTNode'] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "kind": self.kind,
            "value": self.value,
            "children": [c.to_dict() for c in self.children]
        }

def num(v: str): return ASTNode("NUM", v)
def mem(name: str): return ASTNode("MEM", name)
def binop(op: str, a: ASTNode, b: ASTNode): return ASTNode("BINOP", op, [a, b])
def relop(op: str, a: ASTNode, b: ASTNode): return ASTNode("RELOP", op, [a, b])
def rescmd(n: ASTNode): return ASTNode("RESCMD", None, [n])
def memstore(v: ASTNode, m: ASTNode): return ASTNode("MEMSTORE", None, [v, m])
def memload(m: ASTNode): return ASTNode("MEMLOAD", None, [m])
def res(expr: ASTNode): return ASTNode("RES", None, [expr])
def ifnode(c: ASTNode, t: ASTNode, e: ASTNode): return ASTNode("IF", None, [c, t, e])
def whilenode(c: ASTNode, b: ASTNode): return ASTNode("WHILE", None, [c, b])
def block(stmts: List[ASTNode]): return ASTNode("BLOCK", None, stmts)
def program(lst: ASTNode): return ASTNode("PROGRAM", None, [lst])
