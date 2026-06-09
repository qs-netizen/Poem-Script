# poemscript/interpreter.py
import math
from poemscript.environment import Environment, PoemFunction
from poemscript.parser import (
    ProgramNode, PoemDefNode, SayNode, CallNode, LiteralNode, VariableNode,
    SetNode, IfNode, RepeatNode, CompareNode
)

class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        # Define curated artistic color flows globally so functions can resolve them
        self.palettes = {
            "neon": ["#FF007F", "#7B00FF", "#00F9FF", "#00FF66"],
            "sunset": ["#FF4500", "#FF8C00", "#FFD700", "#FF1493"],
            "ocean": ["#000080", "#0000FF", "#008080", "#00CED1"],
            "vintage": ["#8B4513", "#CD853F", "#DEB887", "#D2B48C"]
        }
        self.inject_libraries()

    def inject_libraries(self):
        """Pre-loads Math, Turtle, Time, Random, and Color Palettes into global scope."""
        # ==========================================
        # 1. Math Constants & Functions
        # ==========================================
        self.global_env.define("PI", math.pi)
        self.global_env.define("E", math.e)
        self.global_env.define("sqrt", lambda args: math.sqrt(args[0]))
        self.global_env.define("abs", lambda args: abs(args[0]))
        self.global_env.define("pow", lambda args: math.pow(args[0], args[1]))
        self.global_env.define("sin", lambda args: math.sin(args[0]))
        self.global_env.define("cos", lambda args: math.cos(args[0]))
        self.global_env.define("tan", lambda args: math.tan(args[0]))
        self.global_env.define("floor", lambda args: math.floor(args[0]))
        self.global_env.define("ceil", lambda args: math.ceil(args[0]))

        # ==========================================
        # 2. Turtle Graphics Functions (Stable Canvas Refresh)
        # ==========================================
        import turtle
        def start_canvas(args=None):
            # Completely stable refresh sequence that leaves screen properties intact
            turtle.reset()         # Resets pointer orientation, step counts, and brush positions
            turtle.clear()         # Cleanly wipes drawn vectors off the current window canvas
            turtle.showturtle()    # Ensures tracking indicator is fully visible
            turtle.speed(0)        # Instant refresh rendering speed
            return None
            
        self.global_env.define("setup_turtle", start_canvas)
        self.global_env.define("forward", lambda args: turtle.forward(args[0]))
        self.global_env.define("backward", lambda args: turtle.backward(args[0]))
        self.global_env.define("right", lambda args: turtle.right(args[0]))
        self.global_env.define("left", lambda args: turtle.left(args[0]))
        self.global_env.define("pen_up", lambda args: turtle.penup())
        self.global_env.define("pen_down", lambda args: turtle.pendown())
        self.global_env.define("pen_color", lambda args: turtle.color(str(args[0])))
        self.global_env.define("pen_width", lambda args: turtle.width(args[0]))
        self.global_env.define("done_turtle", lambda args: turtle.done())

        # ==========================================
        # 3. Time & Date Functions
        # ==========================================
        import time
        from datetime import datetime
        self.global_env.define("sleep", lambda args: time.sleep(args[0]))
        self.global_env.define("get_hour", lambda args: datetime.now().hour)
        self.global_env.define("get_year", lambda args: datetime.now().year)
        self.global_env.define("current_timestamp", lambda args: time.time())

        # ==========================================
        # 4. Random Library Functions
        # ==========================================
        import random
        self.global_env.define("random_int", lambda args: random.randint(int(args[0]), int(args[1])))
        self.global_env.define("random_float", lambda args: random.random())

        # ==========================================
        # 5. Color Palette Library Functions
        # ==========================================
        def get_palette_color(args):
            theme = str(args[0]).lower()
            idx = int(args[1])
            theme_list = self.palettes.get(theme, ["black"])
            return theme_list[idx % len(theme_list)]

        def random_hex(args=None):
            return f"#{random.randint(0, 0xFFFFFF):06x}"

        self.global_env.define("get_color", get_palette_color)
        self.global_env.define("get_random_hex", random_hex)

    def interpret(self, root_node):
        if not isinstance(root_node, ProgramNode):
            raise Exception("Interpreter Error: Invalid root configuration")
        for statement in root_node.statements:
            self.execute(statement, self.global_env)

    def execute(self, node, env):
        if node is None: return

        if isinstance(node, PoemDefNode):
            env.define(node.name, PoemFunction(node, env))

        elif isinstance(node, SayNode):
            value = self.evaluate(node.value_node, env)
            env.log_output(str(value))

        elif isinstance(node, SetNode):
            value = self.evaluate(node.value_node, env)
            env.define(node.name, value)

        elif isinstance(node, IfNode):
            cond = self.evaluate(node.condition, env)
            if cond:
                for stmt in node.then_body: self.execute(stmt, env)
            elif node.else_body:
                for stmt in node.else_body: self.execute(stmt, env)

        elif isinstance(node, RepeatNode):
            count = int(self.evaluate(node.count_node, env))
            for _ in range(count):
                for stmt in node.body: self.execute(stmt, env)

        else:
            self.evaluate(node, env)

    def evaluate(self, node, env):
        if isinstance(node, LiteralNode): return node.value

        if isinstance(node, VariableNode):
            value = env.get(node.name)
            if isinstance(value, PoemFunction): return value.call(self, [])
            return value

        if isinstance(node, CompareNode):
            return self.evaluate(node.left, env) == self.evaluate(node.right, env)

        if isinstance(node, CallNode):
            target = env.get(node.name)
            args = [self.evaluate(arg, env) for arg in node.args]
            if isinstance(target, PoemFunction): return target.call(self, args)
            if callable(target): return target(args)
            raise Exception(f"Runtime Error: '{node.name}' cannot be executed")

        raise Exception("Interpreter Error: Unrecognized syntax structure")
