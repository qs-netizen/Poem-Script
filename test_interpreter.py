import unittest
import io
import sys
from unittest.mock import patch

from poemscript.lexer import Lexer
from poemscript.parser import Parser
from poemscript.interpreter import Interpreter
from poemscript.runtime import Environment
from poemscript.errors import RuntimeError

class TestInterpreter(unittest.TestCase):

    def setUp(self):
        self.interpreter = Interpreter()
        self.global_env = self.interpreter.global_env # Access to output buffer

    def _run_poemscript(self, text):
        self.global_env.clear_output() # Clear output buffer before each test
        lexer = Lexer(text)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        self.interpreter.interpret(ast)
        return self.global_env.get_output()

    def test_hello_world(self):
        output = self._run_poemscript('Say "Hello, World"')
        self.assertEqual(output, ['Hello, World'])

    def test_variables_and_output(self):
        text = 'Remember age as 16\nRemember name as "Advik"\nSay age\nSay name'
        output = self._run_poemscript(text)
        self.assertEqual(output, [16, 'Advik'])

    def test_math_operations(self):
        output = self._run_poemscript('Say 5 plus 3')
        self.assertEqual(output, [8])
        
        output = self._run_poemscript('Say 10 minus 2')
        self.assertEqual(output, [8])

        output = self._run_poemscript('Say 4 multiplied by 3')
        self.assertEqual(output, [12])

        output = self._run_poemscript('Say 10 divided by 2')
        self.assertEqual(output, [5.0]) # Division results in float

        # Parser is left-associative, so (10 + 2) * 3 = 12 * 3 = 36
        output = self._run_poemscript('Remember x as 10\nRemember y as 2\nSay x plus y multiplied by 3')
        self.assertEqual(output, [36])

    def test_conditions(self):
        text_true = 'Remember age as 16\nIf age is greater than 13\n    Say "Teenager"\nOtherwise\n    Say "Child"'
        output = self._run_poemscript(text_true)
        self.assertEqual(output, ['Teenager'])

        text_false = 'Remember age as 10\nIf age is greater than 13\n    Say "Teenager"\nOtherwise\n    Say "Child"'
        output = self._run_poemscript(text_false)
        self.assertEqual(output, ['Child'])

        text_nested = (
            'Remember temp as 5\n'
            'If temp is greater than 10\n'
            '    Say "Hot"\n'
            'Otherwise\n'
            '    If temp is less than 0\n'
            '        Say "Cold"\n'
            '    Otherwise\n'
            '        Say "Mild"'
        )
        output = self._run_poemscript(text_nested)
        self.assertEqual(output, ['Mild'])

    def test_loops(self):
        text = 'Repeat 3 times\n    Say "Looping"'
        output = self._run_poemscript(text)
        self.assertEqual(output, ['Looping', 'Looping', 'Looping'])

        text_with_variable = 'Remember counter as 2\nRepeat counter times\n    Say counter\n    Remember counter as counter minus 1'
        output = self._run_poemscript(text_with_variable)
        self.assertEqual(output, [2, 1]) # Counter starts at 2, then becomes 1, then loop ends.

    def test_functions(self):
        text = ('A poem called greet\n    Say "Hello from poem!"\nEnd poem\ngreet')
        output = self._run_poemscript(text)
        self.assertEqual(output, ['Hello from poem!'])

        text_multiple_calls = (
            'A poem called print_star\n    Say "*"\nEnd poem\n'
            'print_star\nprint_star\nprint_star'
        )
        output = self._run_poemscript(text_multiple_calls)
        self.assertEqual(output, ['*', '*', '*'])

    def test_lists_and_for_each(self):
        text = (
            'Remember fruits as\n'
            '    apple\n'
            '    banana\n'
            '    orange\n'
            'For each fruit in fruits\n'
            '    Say "I like"\n'
            '    Say fruit'
        )
        output = self._run_poemscript(text)
        self.assertEqual(output, [
            'I like', 'apple', 'I like', 'banana', 'I like', 'orange'
        ])
        
        text_list_output = ('Remember nums as\n    1\n    2\nSay nums')
        output = self._run_poemscript(text_list_output)
        self.assertEqual(output, ['[1, 2]'])

    def test_scope(self):
        text = (
            'Remember global_var as 10\n'
            'If true\n'
            '    Remember local_var as 20\n'
            '    Say local_var\n'
            '    Say global_var\n'
            'Say global_var\n'
            'Say local_var' # This should cause a RuntimeError
        )
        with self.assertRaises(RuntimeError) as cm:
            self._run_poemscript(text)
        self.assertIn("Variable 'local_var' not found.", str(cm.exception))

    def test_division_by_zero(self):
        with self.assertRaises(RuntimeError) as cm:
            self._run_poemscript('Say 10 divided by 0')
        self.assertIn("Division by zero is not allowed.", str(cm.exception))

    def test_undefined_variable(self):
        with self.assertRaises(RuntimeError) as cm:
            self._run_poemscript('Say undefined_var')
        self.assertIn("Variable 'undefined_var' not found.", str(cm.exception))

    def test_comparison_operators(self):
        output = self._run_poemscript('Say 5 is equal to 5')
        self.assertEqual(output, [True])
        output = self._run_poemscript('Say 5 is equal to 6')
        self.assertEqual(output, [False])
        output = self._run_poemscript('Say 7 greater than 5')
        self.assertEqual(output, [True])
        output = self._run_poemscript('Say 3 less than 5')
        self.assertEqual(output, [True])
        output = self._run_poemscript('Say "apple" is "apple"')
        self.assertEqual(output, [True])

    def test_boolean_literals(self):
        output = self._run_poemscript('Say true')
        self.assertEqual(output, [True])
        output = self._run_poemscript('Say false')
        self.assertEqual(output, [False])

    def test_unary_not_operator(self):
        output = self._run_poemscript('Say not (true)') # Parentheses not supported, but `not true` as expression is.
        self.assertEqual(output, [False])
        output = self._run_poemscript('Say not (5 is greater than 10)')
        self.assertEqual(output, [True])
        output = self._run_poemscript('Remember my_bool as true\nSay not my_bool')
        self.assertEqual(output, [False])

if __name__ == '__main__':
    unittest.main()
