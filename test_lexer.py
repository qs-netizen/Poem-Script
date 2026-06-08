import unittest
from poemscript.lexer import Lexer, Token
from poemscript.errors import LexerError

class TestLexer(unittest.TestCase):

    def test_empty_input(self):
        lexer = Lexer("")
        tokens = lexer.tokenize()
        # Empty input might just yield EOF, or NEWLINE + EOF depending on lexer rules
        # Current lexer adds a NEWLINE if none is present at the very end implicitly.
        # If input is empty, a single NEWLINE followed by EOF is a reasonable default.
        self.assertEqual(tokens, [Token('EOF', None, 1, 1)]) # Corrected based on filtering logic

    def test_hello_world(self):
        text = 'Say "Hello, World"'
        lexer = Lexer(text)
        tokens = lexer.tokenize()
        expected = [
            Token('KEYWORD', 'Say', 1, 1),
            Token('STRING', 'Hello, World', 1, 5),
            Token('EOF', None, 1, 17) # Filtered out implicit newline if not explicitly present
        ]
        self.assertEqual(tokens, expected)

    def test_variables(self):
        text = 'Remember age as 16\nRemember name as "Advik"'
        lexer = Lexer(text)
        tokens = lexer.tokenize()
        expected = [
            Token('KEYWORD', 'Remember', 1, 1),
            Token('IDENTIFIER', 'age', 1, 10),
            Token('KEYWORD', 'as', 1, 14),
            Token('NUMBER', 16, 1, 17),
            Token('NEWLINE', '\n', 1, 19),
            Token('KEYWORD', 'Remember', 2, 1),
            Token('IDENTIFIER', 'name', 2, 10),
            Token('KEYWORD', 'as', 2, 15),
            Token('STRING', 'Advik', 2, 18),
            Token('EOF', None, 2, 25)
        ]
        self.assertEqual(tokens, expected)

    def test_math_operators(self):
        text = 'Remember result as 5 plus 3 multiplied by 2'
        lexer = Lexer(text)
        tokens = lexer.tokenize()
        expected = [
            Token('KEYWORD', 'Remember', 1, 1),
            Token('IDENTIFIER', 'result', 1, 10),
            Token('KEYWORD', 'as', 1, 17),
            Token('NUMBER', 5, 1, 20),
            Token('KEYWORD', 'plus', 1, 22),
            Token('NUMBER', 3, 1, 27),
            Token('KEYWORD', 'multiplied by', 1, 29),
            Token('NUMBER', 2, 1, 43),
            Token('EOF', None, 1, 44)
        ]
        self.assertEqual(tokens, expected)

    def test_conditions_indentation(self):
        text = (
            'If age is greater than 13\n'
            '    Say "Teenager"\n'
            'Otherwise\n'
            '    Say "Child"'
        )
        lexer = Lexer(text)
        tokens = lexer.tokenize()
        expected = [
            Token('KEYWORD', 'If', 1, 1),
            Token('IDENTIFIER', 'age', 1, 4),
            Token('KEYWORD', 'is', 1, 8),
            Token('KEYWORD', 'greater than', 1, 11),
            Token('NUMBER', 13, 1, 24),
            Token('NEWLINE', '\n', 1, 26),
            Token('INDENT', None, 2, 1),
            Token('KEYWORD', 'Say', 2, 5),
            Token('STRING', 'Teenager', 2, 9),
            Token('NEWLINE', '\n', 2, 19),
            Token('DEDENT', None, 3, 1),
            Token('KEYWORD', 'Otherwise', 3, 1),
            Token('NEWLINE', '\n', 3, 10),
            Token('INDENT', None, 4, 1),
            Token('KEYWORD', 'Say', 4, 5),
            Token('STRING', 'Child', 4, 9),
            Token('EOF', None, 4, 16)
        ]
        self.assertEqual(tokens, expected)
    
    def test_loops_indentation(self):
        text = (
            'Repeat 5 times\n'
            '    Say "Hello"'
        )
        lexer = Lexer(text)
        tokens = lexer.tokenize()
        expected = [
            Token('KEYWORD', 'Repeat', 1, 1),
            Token('NUMBER', 5, 1, 8),
            Token('KEYWORD', 'times', 1, 10),
            Token('NEWLINE', '\n', 1, 15),
            Token('INDENT', None, 2, 1),
            Token('KEYWORD', 'Say', 2, 5),
            Token('STRING', 'Hello', 2, 9),
            Token('EOF', None, 2, 16)
        ]
        self.assertEqual(tokens, expected)

    def test_function_definition(self):
        text = (
            'A poem called greet\n'
            '    Say "Hello"\n'
            'End poem'
        )
        lexer = Lexer(text)
        tokens = lexer.tokenize()
        expected = [
            Token('KEYWORD', 'A poem called', 1, 1),
            Token('IDENTIFIER', 'greet', 1, 15),
            Token('NEWLINE', '\n', 1, 20),
            Token('INDENT', None, 2, 1),
            Token('KEYWORD', 'Say', 2, 5),
            Token('STRING', 'Hello', 2, 9),
            Token('NEWLINE', '\n', 2, 16),
            Token('DEDENT', None, 3, 1),
            Token('KEYWORD', 'End poem', 3, 1),
            Token('EOF', None, 3, 9)
        ]
        self.assertEqual(tokens, expected)

    def test_list_definition(self):
        text = (
            'Remember colors as\n'
            '    red\n'
            '    blue\n'
            '    green'
        )
        lexer = Lexer(text)
        tokens = lexer.tokenize()
        expected = [
            Token('KEYWORD', 'Remember', 1, 1),
            Token('IDENTIFIER', 'colors', 1, 10),
            Token('KEYWORD', 'as', 1, 17),
            Token('NEWLINE', '\n', 1, 19),
            Token('INDENT', None, 2, 1),
            Token('IDENTIFIER', 'red', 2, 5),
            Token('NEWLINE', '\n', 2, 8),
            Token('IDENTIFIER', 'blue', 3, 5),
            Token('NEWLINE', '\n', 3, 9),
            Token('IDENTIFIER', 'green', 4, 5),
            Token('EOF', None, 4, 10)
        ]
        self.assertEqual(tokens, expected)

    def test_for_each_loop(self):
        text = (
            'For each color in colors\n'
            '    Say color'
        )
        lexer = Lexer(text)
        tokens = lexer.tokenize()
        expected = [
            Token('KEYWORD', 'For each', 1, 1),
            Token('IDENTIFIER', 'color', 1, 10),
            Token('KEYWORD', 'in', 1, 16),
            Token('IDENTIFIER', 'colors', 1, 19),
            Token('NEWLINE', '\n', 1, 25),
            Token('INDENT', None, 2, 1),
            Token('KEYWORD', 'Say', 2, 5),
            Token('IDENTIFIER', 'color', 2, 9),
            Token('EOF', None, 2, 14)
        ]
        self.assertEqual(tokens, expected)

    def test_comments(self):
        text = '# This is a comment\nSay "Hello" # inline comment\nRemember x as 10'
        lexer = Lexer(text)
        tokens = lexer.tokenize()
        expected = [
            # Comments lines are skipped, but newlines are processed.
            # Newline from line 1 followed by newline from line 2 will be compressed to one by lexer filter.
            Token('KEYWORD', 'Say', 2, 1),
            Token('STRING', 'Hello', 2, 5),
            Token('NEWLINE', '\n', 2, 23),
            Token('KEYWORD', 'Remember', 3, 1),
            Token('IDENTIFIER', 'x', 3, 10),
            Token('KEYWORD', 'as', 3, 12),
            Token('NUMBER', 10, 3, 15),
            Token('EOF', None, 3, 17)
        ]
        self.assertEqual(tokens, expected)

    def test_inconsistent_indentation_error(self):
        text = (
            'If true\n'
            '    Say "True"\n'
            '   Say "Oops" # inconsistent indent
        )
        lexer = Lexer(text)
        with self.assertRaises(LexerError) as cm:
            lexer.tokenize()
        self.assertIn("Inconsistent indentation: Indentation must be multiples of 4 spaces.", str(cm.exception))
    
    def test_nested_indentation(self):
        text = (
            'If a\n'
            '    If b\n'
            '        Say "Nested"\n'
            '    Otherwise\n'
            '        Say "Not B"\n'
            'Otherwise\n'
            '    Say "Not A"'
        )
        lexer = Lexer(text)
        tokens = lexer.tokenize()
        expected = [
            Token('KEYWORD', 'If', 1, 1),
            Token('IDENTIFIER', 'a', 1, 4),
            Token('NEWLINE', '\n', 1, 5),
            Token('INDENT', None, 2, 1),
            Token('KEYWORD', 'If', 2, 5),
            Token('IDENTIFIER', 'b', 2, 8),
            Token('NEWLINE', '\n', 2, 9),
            Token('INDENT', None, 3, 1),
            Token('KEYWORD', 'Say', 3, 9),
            Token('STRING', 'Nested', 3, 13),
            Token('NEWLINE', '\n', 3, 21),
            Token('DEDENT', None, 4, 1),
            Token('KEYWORD', 'Otherwise', 4, 5),
            Token('NEWLINE', '\n', 4, 14),
            Token('INDENT', None, 5, 1),
            Token('KEYWORD', 'Say', 5, 9),
            Token('STRING', 'Not B', 5, 13),
            Token('NEWLINE', '\n', 5, 20),
            Token('DEDENT', None, 6, 1),
            # Lexer emits DEDENT for 'If b' block, then for 'If a' block when indent goes from 4 to 0
            # This is how the lexer detects indentation changes for nested blocks.
            Token('DEDENT', None, 6, 1),
            Token('KEYWORD', 'Otherwise', 6, 1),
            Token('NEWLINE', '\n', 6, 10),
            Token('INDENT', None, 7, 1),
            Token('KEYWORD', 'Say', 7, 5),
            Token('STRING', 'Not A', 7, 9),
            Token('EOF', None, 7, 16)
        ]
        self.assertEqual(tokens, expected)
    
    def test_boolean_literals(self):
        text = 'Say true\nSay false'
        lexer = Lexer(text)
        tokens = lexer.tokenize()
        expected = [
            Token('KEYWORD', 'Say', 1, 1),
            Token('BOOLEAN', True, 1, 5),
            Token('NEWLINE', '\n', 1, 9),
            Token('KEYWORD', 'Say', 2, 1),
            Token('BOOLEAN', False, 2, 5),
            Token('EOF', None, 2, 10)
        ]
        self.assertEqual(tokens, expected)


if __name__ == '__main__':
    unittest.main()
