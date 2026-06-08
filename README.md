# 📜 PoemScript

PoemScript is an elegant, lightweight, indentation-based programming language built with Python. Designed to merge the fluidity of poetry with structural coding patterns, PoemScript replaces verbose braces and structural keywords with minimal indentation rules, clean variables, conditionals, loops, and vibrant built-in libraries.

---

## ✨ Core Features

* **Indentation-Driven Blocks:** No `end` keywords, curly braces `{}`, or semicolons `;`. Code block logic mimics Python's clean aesthetic structure.
* **Intuitive Variable State Scope:** Declare variables seamlessly with `Set <name> to <expression>`.
* **Control Flow Framework:** Robust logical evaluation with `If` / `Else` gates alongside custom iteration loops using `Repeat <count> times`.
* **Native Sub-Routine Definitions:** Encapsulate poetic routines elegantly using the `A poem called <Name>` sequence.
* **Built-In Library Ecosystem:** Direct native support for Math calculation constants, real-time Time clocks, Random generators, and custom Turtle graphics palettes.

---

## 🎨 Code Architecture Examples

### 1. Vector Masterpiece Script (`lpc.poem`)
Combines Loop iterations, Variable trackers, Conditionals, and Palette selection parameters to render generative art safely:

```text
A poem called RunLPC
    Say "--- Matrix Core Architecture Stress Test ---"
    
    setup_turtle()
    pen_width(4)
    
    Set cycle_index to 1
    
    Repeat 4 times
        pen_color(get_color("sunset", cycle_index))
        forward(80)
        right(90)
        Set cycle_index to random_int(1, 4)

RunLPC
