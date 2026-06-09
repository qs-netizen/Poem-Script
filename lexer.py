# poemscript/lexer.py

class Token:
    def __init__(self, type_, value=None, line=1, col=1):
        self.type = type_
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"


class Lexer:
    def __init__(self, text):
        self.text = text
        self.tokens = []
        self.indent_stack = [0]

    def tokenize(self):
        lines = self.text.splitlines()
        
        for i, line_text in enumerate(lines, 1):
            if not line_text.strip() or line_text.strip().startswith('#'):
                continue

            indent = len(line_text) - len(line_text.lstrip())
            line_content = line_text.lstrip()

            if indent > self.indent_stack[-1]:
                self.tokens.append(Token('INDENT', indent, i, 1))
                self.indent_stack.append(indent)
            elif indent < self.indent_stack[-1]:
                while indent < self.indent_stack[-1]:
                    self.tokens.append(Token('DEDENT', self.indent_stack[-1], i, 1))
                    self.indent_stack.pop()
                if indent != self.indent_stack[-1]:
                    raise Exception(f"Indentation error on line {i}")

            idx = 0
            while idx < len(line_content):
                char = line_content[idx]

                if char.isspace():
                    idx += 1
                    continue

                if char == '"':
                    start_col = idx + 1
                    val = ""
                    idx += 1
                    while idx < len(line_content) and line_content[idx] != '"':
                        val += line_content[idx]
                        idx += 1
                    if idx >= len(line_content):
                        raise Exception(f"Unterminated string on line {i}")
                    idx += 1
                    self.tokens.append(Token('STRING', val, i, start_col))
                    continue

                # Comparison Operator
                if char == '=' and idx + 1 < len(line_content) and line_content[idx + 1] == '=':
                    self.tokens.append(Token('EQUALS', '==', i, idx + 1))
                    idx += 2
                    continue

                if char == '(':
                    self.tokens.append(Token('LPAREN', '(', i, idx + 1))
                    idx += 1
                    continue
                if char == ')':
                    self.tokens.append(Token('RPAREN', ')', i, idx + 1))
                    idx += 1
                    continue
                if char == ',':
                    self.tokens.append(Token('COMMA', ',', i, idx + 1))
                    idx += 1
                    continue

                if char.isdigit() or char == '.':
                    start_col = idx + 1
                    num_str = ""
                    while idx < len(line_content) and (line_content[idx].isdigit() or line_content[idx] == '.'):
                        num_str += line_content[idx]
                        idx += 1
                    self.tokens.append(Token('NUMBER', float(num_str) if '.' in num_str else int(num_str), i, start_col))
                    continue

                if char.isalpha() or char == '_':
                    start_col = idx + 1
                    ident = ""
                    while idx < len(line_content) and (line_content[idx].isalnum() or line_content[idx] == '_'):
                        ident += line_content[idx]
                        idx += 1
                    
                    # Language Keywords
                    if ident == 'Set': self.tokens.append(Token('SET', ident, i, start_col))
                    elif ident == 'to': self.tokens.append(Token('TO', ident, i, start_col))
                    elif ident == 'If': self.tokens.append(Token('IF', ident, i, start_col))
                    elif ident == 'Else': self.tokens.append(Token('ELSE', ident, i, start_col))
                    elif ident == 'Repeat': self.tokens.append(Token('REPEAT', ident, i, start_col))
                    elif ident == 'times': self.tokens.append(Token('TIMES', ident, i, start_col))
                    else: self.tokens.append(Token('IDENTIFIER', ident, i, start_col))
                    continue

                raise Exception(f"Unexpected character '{char}' (line {i}, column {idx + 1})")

            self.tokens.append(Token('NEWLINE', '\n', i, len(line_text) + 1))

        while len(self.indent_stack) > 1:
            self.tokens.append(Token('DEDENT', self.indent_stack[-1], len(lines), 1))
            self.indent_stack.pop()
            
        self.tokens.append(Token('EOF', None, len(lines), 1))
        return self.tokens
