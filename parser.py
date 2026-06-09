# poemscript/parser.py

class ASTNode:
    def __init__(self, line=1): self.line = line

class ProgramNode(ASTNode):
    def __init__(self, statements, line=1):
        super().__init__(line)
        self.statements = statements

class PoemDefNode(ASTNode):
    def __init__(self, name, body, line=1):
        super().__init__(line)
        self.name = name
        self.body = body

class SayNode(ASTNode):
    def __init__(self, value_node, line=1):
        super().__init__(line)
        self.value_node = value_node

class SetNode(ASTNode):
    def __init__(self, name, value_node, line=1):
        super().__init__(line)
        self.name = name
        self.value_node = value_node

class IfNode(ASTNode):
    def __init__(self, condition, then_body, else_body=None, line=1):
        super().__init__(line)
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body

class RepeatNode(ASTNode):
    def __init__(self, count_node, body, line=1):
        super().__init__(line)
        self.count_node = count_node
        self.body = body

class CompareNode(ASTNode):
    def __init__(self, left, right, line=1):
        super().__init__(line)
        self.left = left
        self.right = right

class CallNode(ASTNode):
    def __init__(self, name, args, line=1):
        super().__init__(line)
        self.name = name
        self.args = args

class LiteralNode(ASTNode):
    def __init__(self, value, line=1):
        super().__init__(line)
        self.value = value

class VariableNode(ASTNode):
    def __init__(self, name, line=1):
        super().__init__(line)
        self.name = name


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    @property
    def current_token(self): return self.tokens[self.pos]

    def consume(self, token_type=None):
        tok = self.current_token
        if token_type and tok.type != token_type:
            raise Exception(f"Syntax Error: Expected {token_type}, got {tok.type} on line {tok.line}")
        self.pos += 1
        return tok

    def peek(self, distance=1):
        if self.pos + distance >= len(self.tokens): return self.tokens[-1]
        return self.tokens[self.pos + distance]

    def parse(self):
        statements = []
        start_line = self.current_token.line if self.tokens else 1
        while self.current_token.type != 'EOF':
            if self.current_token.type == 'NEWLINE':
                self.consume('NEWLINE')
                continue
            statements.append(self.parse_statement())
        return ProgramNode(statements, line=start_line)

    def parse_statement(self):
        tok = self.current_token

        # Poem Def: A poem called <Name>
        if tok.type == 'IDENTIFIER' and tok.value == 'A':
            if self.peek(1).value == 'poem' and self.peek(2).value == 'called':
                start_line = tok.line
                self.consume(); self.consume(); self.consume()
                name = self.consume('IDENTIFIER').value
                self.consume('NEWLINE')
                return PoemDefNode(name, self.parse_block(), line=start_line)

        # Say Statement
        if tok.type == 'IDENTIFIER' and tok.value == 'Say':
            start_line = tok.line
            self.consume()
            expr = self.parse_expression()
            self.consume('NEWLINE')
            return SayNode(expr, line=start_line)

        # Set Statement: Set x to 10
        if tok.type == 'SET':
            start_line = tok.line
            self.consume('SET')
            var_name = self.consume('IDENTIFIER').value
            self.consume('TO')
            expr = self.parse_expression()
            self.consume('NEWLINE')
            return SetNode(var_name, expr, line=start_line)

        # If Statement: If condition
        if tok.type == 'IF':
            start_line = tok.line
            self.consume('IF')
            condition = self.parse_expression()
            self.consume('NEWLINE')
            then_body = self.parse_block()
            else_body = None
            if self.current_token.type == 'ELSE':
                self.consume('ELSE')
                self.consume('NEWLINE')
                else_body = self.parse_block()
            return IfNode(condition, then_body, else_body, line=start_line)

        # Repeat Loop: Repeat 4 times
        if tok.type == 'REPEAT':
            start_line = tok.line
            self.consume('REPEAT')
            count_node = self.parse_expression()
            self.consume('TIMES')
            self.consume('NEWLINE')
            body = self.parse_block()
            return RepeatNode(count_node, body, line=start_line)

        expr = self.parse_expression()
        self.consume('NEWLINE')
        return expr

    def parse_block(self):
        self.consume('INDENT')
        body = []
        while self.current_token.type != 'DEDENT' and self.current_token.type != 'EOF':
            if self.current_token.type == 'NEWLINE':
                self.consume('NEWLINE')
                continue
            body.append(self.parse_statement())
        self.consume('DEDENT')
        return body

    def parse_expression(self):
        left = self.parse_primary_expression()
        if self.current_token.type == 'EQUALS':
            start_line = self.current_token.line
            self.consume('EQUALS')
            right = self.parse_primary_expression()
            return CompareNode(left, right, line=start_line)
        return left

    def parse_primary_expression(self):
        tok = self.current_token
        if tok.type in ('NUMBER', 'STRING'):
            self.consume()
            return LiteralNode(tok.value, line=tok.line)
        if tok.type == 'IDENTIFIER':
            name = self.consume('IDENTIFIER').value
            if self.current_token.type == 'LPAREN':
                self.consume('LPAREN')
                args = []
                if self.current_token.type != 'RPAREN':
                    args.append(self.parse_expression())
                    while self.current_token.type == 'COMMA':
                        self.consume('COMMA')
                        args.append(self.parse_expression())
                self.consume('RPAREN')
                return CallNode(name, args, line=tok.line)
            return VariableNode(name, line=tok.line)
        raise Exception(f"Syntax Error: Unexpected element '{tok.value}' on line {tok.line}")
