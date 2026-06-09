# poemscript/math_lib.py
import math

class PoemMathLibrary:
    @staticmethod
    def inject(env):
        """Injects math constants and functions into the given environment."""
        
        # 1. Register Constants
        env.define("PI", math.pi)
        env.define("E", math.e)
        
        # 2. Register Functions
        # We wrap Python functions so your interpreter can call them
        env.define("sqrt", lambda args: math.sqrt(args[0]))
        env.define("abs", lambda args: abs(args[0]))
        env.define("pow", lambda args: math.pow(args[0], args[1]))
        env.define("sin", lambda args: math.sin(args[0]))
        env.define("cos", lambda args: math.cos(args[0]))
        env.define("tan", lambda args: math.tan(args[0]))
        env.define("floor", lambda args: math.floor(args[0]))
        env.define("ceil", lambda args: math.ceil(args[0]))
        
        return env
