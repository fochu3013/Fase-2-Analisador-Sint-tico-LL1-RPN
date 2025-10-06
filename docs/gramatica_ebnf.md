Terminais (tokens):
```
LPAREN='('  RPAREN=')'
NUM: [0-9]+(\.[0-9]+)?
MEM: [A-Z]+              # memórias em maiúsculas
ID : [A-Za-z_][A-Za-z0-9_]*  # usado internamente; MEM ⊂ ID
OP  : '+' | '-' | '*' | '|' | '/' | '%' | '^'
RELOP: '>' | '<' | '>=' | '<=' | '==' | '!='
RES : 'RES'
IF  : 'IF'
WHILE: 'WHILE'
EOF
```

Não-terminais principais:
```
PROGRAM   → LIST EOF
LIST      → STMT LIST | ε
STMT      → EXPR | IF_STMT | WHILE_STMT
EXPR      → NUM
          | MEMLOAD              # (MEM)
          | RESCMD               # (N RES)
          | MEMSTORE             # (V MEM)
          | '(' EXPR EXPR OP ')' # binária RPN
          | '(' EXPR RES ')'     # print RPN (alternativo, opcional)
COND      → '(' EXPR EXPR RELOP ')'
BLOCK     → '(' LIST ')'
IF_STMT   → '(' COND BLOCK BLOCK IF ')'
WHILE_STMT→ '(' COND BLOCK WHILE ')'
MEMLOAD   → '(' MEM ')'
RESCMD    → '(' NUM RES ')'
MEMSTORE  → '(' NUM MEM ')'
```

**Observações LL(1):**
- `LIST` usa lookahead `{NUM, LPAREN}` para derivar `STMT LIST`, senão `ε` (quando `RPAREN` ou `EOF`).
- Discriminação de formas entre parênteses é feita pelo **padrão interno** (`RES` no fim → `RESCMD`, `MEM` como segundo item → `MEMSTORE`, só `MEM` → `MEMLOAD`, `OP` no fim → binária, `IF/WHILE` nos casos de controle).
- `|` é **divisão real**; `/` é **divisão inteira** 


