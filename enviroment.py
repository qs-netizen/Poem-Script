# poemscript/environment.py
import math

class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent
        self.output_log = []

    def define(self, name, value):
        self.variables[name] = value

    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name)
        raise Exception(f"Runtime Error: Undefined identifier '{name}'")

    def log_output(self, text):
        if self.parent:
            self.parent.log_output(text)
        else:
            self.output_log.append(text)

    def get_output(self):
        return self.output_log


class PoemFunction:
    def __init__(self, node, env):
        self.node = node  # The PoemDefNode
        self.closure = env

    def call(self, interpreter, args):
        # We pass the running interpreter instance directly as an argument 
        # instead of importing it at the top of the file!
        local_env = Environment(self.closure)
        for statement in self.node.body:
            interpreter.execute(statement, local_env)
        return None
