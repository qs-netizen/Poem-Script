from poemscript.lexer import Lexer
from poemscript.parser import Parser
from poemscript.interpreter import Interpreter


code = """
Remember colors as
    red
    blue
    green

For each color in colors
    Say color
"""

print("LEXER START")
lexer = Lexer(code)
tokens = lexer.tokenize()
print("LEXER DONE")

for t in tokens:
    print(t)

print("PARSER START")
parser = Parser(tokens)
ast = parser.parse()
print("PARSER DONE")

print(ast)
print("INTERPRETER START")

interpreter = Interpreter()
interpreter.interpret(ast)

print("INTERPRETER DONE")
print(interpreter.global_env.get_output())
def visit_ListLiteral(self, node):
    interpreted_elements = []

    for element_node in node.elements:
        print("LIST ELEMENT:", element_node)

        if isinstance(element_node, Identifier):
            interpreted_elements.append(element_node.name)
        else:
            interpreted_elements.append(
                self.interpret(element_node)
            )

    print("FINAL LIST:", interpreted_elements)

    return interpreted_elements
