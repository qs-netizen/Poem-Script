from collections import deque
from poemscript.errors import RuntimeError

class Environment:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent
        self.output_buffer = deque() # For capturing 'Say' output in tests

    def define(self, name, value):
        if name in self.symbols:
            # Allow re-definition within loops (e.g. `Repeat N times 
            #   Remember counter as ...`) as it's common in poetic contexts.
            # For now, it's a soft re-definition. More robust error handling needed for production.
            self.symbols[name] = value 
            # raise RuntimeError(f"Variable '{name}' is already defined in this scope.")
        self.symbols[name] = value

    def assign(self, name, value):
        if name in self.symbols:
            self.symbols[name] = value
            return
        if self.parent:
            self.parent.assign(name, value)
            return
        raise RuntimeError(f"Variable '{name}' not found.")

    def lookup(self, name):
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        raise RuntimeError(f"Variable '{name}' not found.")

    def push_output(self, value):
        self.output_buffer.append(value)

    def pop_output(self):
        if self.output_buffer:
            return self.output_buffer.popleft()
        return None # or raise error

    def get_output(self):
        return list(self.output_buffer)

    def clear_output(self):
        self.output_buffer.clear()

