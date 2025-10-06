// Gabriel Fischer domakoski
// Nome do grupo no Canvas: [RA2 7]

# Fase 2 – Analisador Sintático LL(1) (RPN)

### 1) Modo *source* 
```bash
python src/main.py tests/teste1.rpn -o ast_out.json
```

### 2) Modo *tokens* 
```bash
python src/main.py dummy -o ast_out.json --input-tokens tests/tokens1.json
```
Formato esperado (JSON): array de objetos `{type, lexeme, line, col}`. O leitor aceita **várias convenções** comuns da Fase 1:
- `LPAREN/RPAREN`, `NUM`, `ID` (converte **ID em maiúsculas** para `MEM` automaticamente).
- Ops como `PLUS/MINUS/TIMES/DIVI/DIVR/MOD/POW` ou símbolos `+ - * / | % ^`.
- Relops como `GT/LT/GE/LE/EQ/NE` ou símbolos `> < >= <= == !=`.
- Keywords: `RES`, `IF`, `WHILE`.
- Garante `EOF` ao fim se ausente.

## Regras suportadas

- **Aritmética RPN**: `+ - * | / % ^` (`|` divisão real; `/` divisão inteira).
- **Comandos especiais (Fase 1)**: `(N RES)`, `(V MEM)`, `(MEM)` — `MEM` em maiúsculas.
- **Controle (Fase 2)**:
  - `IF`: `( COND BLOCK BLOCK IF )`
  - `WHILE`: `( COND BLOCK WHILE )`
  - `COND`: `( EXPR EXPR RELOP )`
  - `BLOCK`: `( LIST )`

## Estrutura
```
/src
  tokens.py, lexer_io.py, token_io.py
  ast_nodes.py, parser_ll1.py, api_wrappers.py, errors.py, main.py
/docs
  gramatica_ebnf.md, arvore_ultima_execucao.md
/tests
  teste1.rpn, teste2.rpn, teste3.rpn, tokens1.json
```

## Test
```bash
# Source mode
python src/main.py tests/teste2.rpn -o ast_teste2.json

# Tokens mode (exemplo de token vector gerado)
python src/main.py dummy -o ast_tokens.json --input-tokens tests/tokens1.json
```

## Saída
AST em JSON no arquivo passado por `-o` e também uma amostra em `docs/arvore_ultima_execucao.md`.

## Execução
```
AnalisadorSintatico tests\teste1.rpn -o ast_teste1.json
```
