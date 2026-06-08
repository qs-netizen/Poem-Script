import unittest
import subprocess
import sys
import os

# Helper to find the poemscript executable via python -m
cli_command = [sys.executable, '-m', 'poemscript.cli']

class TestCLI(unittest.TestCase):

    def _run_cli(self, filepath):
        cmd = cli_command + [filepath]
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        return result.stdout.strip(), result.stderr.strip(), result.returncode

    def test_hello_world_example(self):
        stdout, stderr, returncode = self._run_cli('examples/hello.poem')
        self.assertEqual(returncode, 0)
        self.assertEqual(stdout, 'Hello, World')
        self.assertEqual(stderr, '')

    def test_variables_example(self):
        stdout, stderr, returncode = self._run_cli('examples/variables.poem')
        self.assertEqual(returncode, 0)
        self.assertIn('Age:\n16\nName:\nAdvik', stdout)
        self.assertEqual(stderr, '')

    def test_conditions_example(self):
        stdout, stderr, returncode = self._run_cli('examples/conditions.poem')
        self.assertEqual(returncode, 0)
        self.assertIn('Teenager\n---\nThe weather is pleasant.', stdout)
        self.assertEqual(stderr, '')

    def test_loops_example(self):
        stdout, stderr, returncode = self._run_cli('examples/loops.poem')
        self.assertEqual(returncode, 0)
        self.assertIn('Counting down:\n3\n2\n1\nLift off!\n---\nRepeating Hello:\nHello\nHello', stdout)
        self.assertEqual(stderr, '')

    def test_functions_example(self):
        stdout, stderr, returncode = self._run_cli('examples/functions.poem')
        self.assertEqual(returncode, 0)
        self.assertIn('Calling the poem:\nHello from poem!\nI speak in verses.\n--- Another poem ---\n--------------------', stdout)
        self.assertEqual(stderr, '')

    def test_lists_example(self):
        stdout, stderr, returncode = self._run_cli('examples/lists.poem')
        self.assertEqual(returncode, 0)
        self.assertIn('My favorite colors:\nred\nblue\ngreen\n---\nSumming numbers:\nTotal sum is:\n60\n---\nFull list:\n[10, 20, 30]', stdout)
        self.assertEqual(stderr, '')

    def test_comprehensive_example(self):
        stdout, stderr, returncode = self._run_cli('examples/comprehensive.poem')
        self.assertEqual(returncode, 0)
        self.assertIn('Welcome to the world of\nPoemScript\nby\nAI Architect', stdout)
        self.assertIn('The number is positive.', stdout)
        self.assertIn('Counting:\n1\nCounting:\n2\nCounting:\n3', stdout)
        self.assertIn('Found my favorite fruit:\napple\nMy favorite fruit was among those available.', stdout)
        self.assertEqual(stderr, '')

    def test_file_not_found(self):
        stdout, stderr, returncode = self._run_cli('non_existent.poem')
        self.assertEqual(returncode, 1)
        self.assertEqual(stdout, '')
        self.assertIn('Error: File not found at', stderr)

    def test_syntax_error(self):
        # Create a temporary file with a syntax error
        error_poem_content = 'Say "Hello" MissingQuote\n'
        temp_file = 'temp_error.poem'
        with open(temp_file, 'w') as f:
            f.write(error_poem_content)
        
        stdout, stderr, returncode = self._run_cli(temp_file)
        os.remove(temp_file)

        self.assertEqual(returncode, 1)
        self.assertEqual(stdout, '')
        self.assertIn("Unexpected character 'M'", stderr) # Lexer catches this as it's not a valid token

    def test_runtime_error(self):
        # Create a temporary file with a runtime error (e.g., undefined variable)
        error_poem_content = 'Say undefined_var'
        temp_file = 'temp_runtime_error.poem'
        with open(temp_file, 'w') as f:
            f.write(error_poem_content)

        stdout, stderr, returncode = self._run_cli(temp_file)
        os.remove(temp_file)

        self.assertEqual(returncode, 1)
        self.assertEqual(stdout, '')
        self.assertIn("Variable 'undefined_var' not found.", stderr)

if __name__ == '__main__':
    unittest.main()
