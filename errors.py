# poemscript/errors.py

class PoemScriptError(Exception):
    def __init__(self, message, line=None, column=None):
        self.message = message
        self.line = line
        self.column = column

        if line is not None and column is not None:
            super().__init__(
                f"{message} (line {line}, column {column})"
            )
        else:
            super().__init__(message)


class LexerError(PoemScriptError):
    print("LexerError")
    pass


class ParserError(PoemScriptError):
    print("ParserError")
    pass


class RuntimeError(PoemScriptError):
    print("RuntimeError")
    pass
