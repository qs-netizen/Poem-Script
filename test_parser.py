import unittest
from poemscript.lexer import Lexer, Token
from poemscript.parser import Parser
from poemscript.ast import (
    Program, SayStatement, RememberStatement, IfStatement, RepeatStatement,
    FunctionDefinition, FunctionCall, ForStatement, ListLiteral,
    NumberLiteral, StringLiteral, BooleanLiteral, Identifier, BinaryOperation, UnaryOperation
)
from poemscript.errors import ParserError

class TestParser(unittest.TestCase):

    def _parse_text(self, text):
        lexer = Lexer(text)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        return parser.parse()

    def test_parse_hello_world(self):
        ast = self._parse_text('Say "Hello, World"')
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.statements), 1)
        self.assertIsInstance(ast.statements[0], SayStatement)
        self.assertIsInstance(ast.statements[0].expression, StringLiteral)
        self.assertEqual(ast.statements[0].expression.value, 'Hello, World')

    def test_parse_variables(self):
        ast = self._parse_text('Remember age as 16\nRemember name as "Advik"')
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.statements), 2)
        
        self.assertIsInstance(ast.statements[0], RememberStatement)
        self.assertEqual(ast.statements[0].name, 'age')
        self.assertIsInstance(ast.statements[0].value, NumberLiteral)
        self.assertEqual(ast.statements[0].value.value, 16)

        self.assertIsInstance(ast.statements[1], RememberStatement)
        self.assertEqual(ast.statements[1].name, 'name')
        self.assertIsInstance(ast.statements[1].value, StringLiteral)
        self.assertEqual(ast.statements[1].value.value, 'Advik')

    def test_parse_math(self):
        ast = self._parse_text('Say 5 plus 3')
        self.assertIsInstance(ast.statements[0], SayStatement)
        expr = ast.statements[0].expression
        self.assertIsInstance(expr, BinaryOperation)
        self.assertEqual(expr.operator, 'plus')
        self.assertIsInstance(expr.left, NumberLiteral)
        self.assertEqual(expr.left.value, 5)
        self.assertIsInstance(expr.right, NumberLiteral)
        self.assertEqual(expr.right.value, 3)

        ast = self._parse_text('Say 10 minus 2 multiplied by 3') # Parses left-associative, (10 - 2) * 3
        expr = ast.statements[0].expression
        self.assertIsInstance(expr, BinaryOperation)
        self.assertEqual(expr.operator, 'multiplied by')
        self.assertIsInstance(expr.right, NumberLiteral)
        self.assertEqual(expr.right.value, 3)
        
        left_of_mult = expr.left
        self.assertIsInstance(left_of_mult, BinaryOperation)
        self.assertEqual(left_of_mult.operator, 'minus')
        self.assertIsInstance(left_of_mult.left, NumberLiteral)
        self.assertEqual(left_of_mult.left.value, 10)
        self.assertIsInstance(left_of_mult.right, NumberLiteral)
        self.assertEqual(left_of_mult.right.value, 2)

    def test_parse_conditions(self):
        text = (
            'If age is greater than 13\n'
            '    Say "Teenager"\n'
            'Otherwise\n'
            '    Say "Child"'
        )
        ast = self._parse_text(text)
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.statements), 1)
        if_stmt = ast.statements[0]
        self.assertIsInstance(if_stmt, IfStatement)
        self.assertIsInstance(if_stmt.condition, BinaryOperation)
        self.assertEqual(if_stmt.condition.operator, 'greater than')
        self.assertEqual(len(if_stmt.body), 1)
        self.assertEqual(len(if_stmt.otherwise_body), 1)
        self.assertIsInstance(if_stmt.body[0], SayStatement)
        self.assertIsInstance(if_stmt.otherwise_body[0], SayStatement)

    def test_parse_loops(self):
        text = 'Repeat 5 times\n    Say "Hello"'
        ast = self._parse_text(text)
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.statements), 1)
        repeat_stmt = ast.statements[0]
        self.assertIsInstance(repeat_stmt, RepeatStatement)
        self.assertIsInstance(repeat_stmt.count_expression, NumberLiteral)
        self.assertEqual(repeat_stmt.count_expression.value, 5)
        self.assertEqual(len(repeat_stmt.body), 1)
        self.assertIsInstance(repeat_stmt.body[0], SayStatement)

    def test_parse_functions(self):
        text = (
            'A poem called greet\n'
            '    Say "Hello"\n'
            'End poem\n'
            'greet'
        )
        ast = self._parse_text(text)
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.statements), 2)
        
        func_def = ast.statements[0]
        self.assertIsInstance(func_def, FunctionDefinition)
        self.assertEqual(func_def.name, 'greet')
        self.assertEqual(len(func_def.body), 1)
        self.assertIsInstance(func_def.body[0], SayStatement)

        func_call = ast.statements[1]
        self.assertIsInstance(func_call, FunctionCall)
        self.assertEqual(func_call.name, 'greet')

    def test_parse_lists(self):
        text = (
            'Remember colors as\n'
            '    red\n'
            '    blue\n'
            '    green'
        )
        ast = self._parse_text(text)
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.statements), 1)
        list_stmt = ast.statements[0]
        self.assertIsInstance(list_stmt, RememberStatement)
        self.assertEqual(list_stmt.name, 'colors')
        self.assertIsInstance(list_stmt.value, ListLiteral)
        self.assertEqual(len(list_stmt.value.elements), 3)
        self.assertIsInstance(list_stmt.value.elements[0], Identifier) # Elements are identifiers at parse stage
        self.assertEqual(list_stmt.value.elements[0].name, 'red')
        self.assertIsInstance(list_stmt.value.elements[1], Identifier)
        self.assertEqual(list_stmt.value.elements[1].name, 'blue')

    def test_parse_for_each(self):
        text = (
            'For each color in colors\n'
            '    Say color'
        )
        ast = self._parse_text(text)
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.statements), 1)
        for_stmt = ast.statements[0]
        self.assertIsInstance(for_stmt, ForStatement)
        self.assertEqual(for_stmt.item_variable, 'color')
        self.assertEqual(for_stmt.iterable_variable, 'colors')
        self.assertEqual(len(for_stmt.body), 1)
        self.assertIsInstance(for_stmt.body[0], SayStatement)

    def test_parser_error_unexpected_token(self):
        with self.assertRaises(ParserError) as cm:
            self._parse_text('Say +') # '+' is not a recognized operator token or primary expression start
        self.assertIn("Unexpected character", str(cm.exception)) # Lexer catches first.

        with self.assertRaises(ParserError) as cm:
            self._parse_text('Remember x 10') # Missing 'as'
        self.assertIn("Expected 'KEYWORD' with value \"as\", got 'NUMBER'", str(cm.exception))

    def test_parse_unary_not(self):
        text = 'Say not true'
        ast = self._parse_text(text)
        self.assertIsInstance(ast.statements[0], SayStatement)
        expr = ast.statements[0].expression
        self.assertIsInstance(expr, UnaryOperation)
        self.assertEqual(expr.operator, 'not')
        self.assertIsInstance(expr.operand, BooleanLiteral)
        self.assertEqual(expr.operand.value, True)

    def test_parse_boolean_literals(self):
        ast = self._parse_text('Say true')
        self.assertIsInstance(ast.statements[0].expression, BooleanLiteral)
        self.assertEqual(ast.statements[0].expression.value, True)

        ast = self._parse_text('Say false')
        self.assertIsInstance(ast.statements[0].expression, BooleanLiteral)
        self.assertEqual(ast.statements[0].expression.value, False)


if __name__ == '__main__':
    unittest.main()
