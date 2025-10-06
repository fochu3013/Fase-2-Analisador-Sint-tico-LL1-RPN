import argparse, json, sys, os
from .api_wrappers import lerTokens, lerTokensDeArquivoJSON, construirGramatica, parsear, gerarArvore
from .errors import ParseError

def main():
    ap = argparse.ArgumentParser(description="Fase 2 – Parser LL(1) (RPN)")
    ap.add_argument("input", help="arquivo de entrada .rpn (modo 'source') ou um dummy quando usar --input-tokens")
    ap.add_argument("-o", "--output", default="ast_out.json", help="arquivo de saída (AST em JSON)")
    ap.add_argument("--input-tokens", help="caminho para JSON com vetor de tokens da Fase 1 (ignora 'input' como fonte)")
    args = ap.parse_args()

    try:
        if args.input_tokens:
            tokens = lerTokensDeArquivoJSON(args.input_tokens)
        else:
            with open(args.input, "r", encoding="utf-8") as f:
                text = f.read()
            tokens = lerTokens(text)

        _g = construirGramatica()
        ast = parsear(tokens)
        tree = gerarArvore(ast)
        with open(args.output, "w", encoding="utf-8") as o:
            json.dump(tree, o, ensure_ascii=False, indent=2)
        print(f"AST salva em {args.output}")
    except ParseError as e:
        print(f"Erro de sintaxe: {e}", file=sys.stderr); sys.exit(2)
    except SyntaxError as e:
        print(f"Erro léxico: {e}", file=sys.stderr); sys.exit(3)
    except OSError as e:
        print(f"Erro de E/S: {e}", file=sys.stderr); sys.exit(1)

if __name__ == "__main__":
    main()
