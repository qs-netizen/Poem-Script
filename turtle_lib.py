# poemscript/turtle_lib.py
import turtle

class PoemTurtleLibrary:
    @staticmethod
    def inject(env):
        """Injects visual turtle graphic functions into the environment."""
        
        # 1. Window & Initialization
        # We force a reset so running the code multiple times doesn't crash the studio
        def start_canvas(args=None):
            turtle.ResetableTurtle._screen = None
            turtle.Turtle._screen = None
            turtle.clearscreen()
            turtle.showturtle()
            turtle.speed(3)
            return None

        env.define("setup_turtle", start_canvas)
        env.define("done_turtle", lambda args: turtle.done())

        # 2. Vector Movement 
        env.define("forward", lambda args: turtle.forward(args[0]))
        env.define("backward", lambda args: turtle.backward(args[0]))
        env.define("right",    lambda args: turtle.right(args[0]))
        env.define("left",     lambda args: turtle.left(args[0]))
        
        # 3. Aesthetics & Properties
        env.define("pen_up",    lambda args: turtle.penup())
        env.define("pen_down",  lambda args: turtle.pendown())
        env.define("pen_color", lambda args: turtle.color(str(args[0])))
        env.define("pen_width", lambda args: turtle.width(args[0]))
        
        return env
