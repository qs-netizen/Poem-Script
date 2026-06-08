import argparse
import sys

from poemscript.lexer import Lexer
from poemscript.parser import Parser
from poemscript.interpreter import Interpreter
from poemscript.errors import PoemScriptError, LexerError, ParserError, RuntimeError

def run_poemscript_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        
        lexer = Lexer(text)
        tokens = lexer.tokenize()
        
        # print("\n--- TOKENS ---")
        # for token in tokens:
        #     print(token)
        # print("--------------\n")

        parser = Parser(tokens)
        ast = parser.parse()

        # For debugging AST structure
        # import json
        # from dataclasses import asdict
        # print("\n--- AST ---")
        # print(json.dumps(asdict(ast), indent=2))
        # print("-----------\n")

        interpreter = Interpreter()
        interpreter.interpret(ast)

    except (LexerError, ParserError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: File not found at '{filepath}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        prog='poemscript',
        description='Run a PoemScript file, a language designed for poetic expression.',
        epilog='Example: poemscript examples/hello.poem'
    )
    parser.add_argument('file', type=str, help='Path to the PoemScript file to execute.')
    
    args = parser.parse_args()
    run_poemscript_file(args.file)

if __name__ == '__main__':
    main()
