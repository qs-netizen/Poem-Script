import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path

# Assuming these modules are in your local directory structure
from poemscript.lexer import Lexer
from poemscript.parser import Parser
from poemscript.interpreter import Interpreter

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class PoemScriptStudio(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("🌸 PoemScript Studio")
        self.geometry("1400x850")

        self.examples_dir = Path("examples")

        self.build_ui()

    def build_ui(self):

        # Header
        header = ctk.CTkFrame(self, height=70)
        header.pack(fill="x", padx=10, pady=10)

        title = ctk.CTkLabel(
            header,
            text="🌸 PoemScript Studio & PoemScript-Made By Advik Sharma",
            font=("Segoe UI", 28, "bold")
        )
        title.pack(side="left", padx=20, pady=15)

        # Main Area
        main = ctk.CTkFrame(self)
        main.pack(fill="both", expand=True, padx=10, pady=5)

        # Sidebar
        sidebar = ctk.CTkFrame(main, width=250)
        sidebar.pack(side="left", fill="y", padx=(0, 10))

        ctk.CTkLabel(
            sidebar,
            text="Files",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=10)

        self.example_list = ctk.CTkScrollableFrame(sidebar)
        self.example_list.pack(fill="both", expand=True, padx=10)

        self.load_examples()

        ctk.CTkButton(
            sidebar,
            text="📂 Open File",
            command=self.open_file
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            sidebar,
            text="💾 Save File",
            command=self.save_file
        ).pack(fill="x", padx=10, pady=5)

        # Editor Section
        editor_frame = ctk.CTkFrame(main)
        editor_frame.pack(side="left", fill="both", expand=True)

        toolbar = ctk.CTkFrame(editor_frame, height=50)
        toolbar.pack(fill="x", padx=5, pady=5)

        ctk.CTkButton(
            toolbar,
            text="▶ Run",
            width=120,
            command=self.run_code
        ).pack(side="left", padx=5)

        # FIX: Added a command to clear the editor so it doesn't crash on Python 3.14
        ctk.CTkButton(
            toolbar,
            text="🗑 Clear",
            command=self.clear_editor
        ).pack(side="left", padx=5)

        self.editor = ctk.CTkTextbox(
            editor_frame,
            font=("Consolas", 16)
        )
        self.editor.pack(fill="both", expand=True, padx=5, pady=5)

        # Output Section
        output_frame = ctk.CTkFrame(main, width=350)
        output_frame.pack(side="right", fill="both")

        ctk.CTkLabel(
            output_frame,
            text="Console",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=10)

        self.output = ctk.CTkTextbox(
            output_frame,
            font=("Consolas", 14)
        )
        self.output.pack(fill="both", expand=True, padx=10, pady=10)

        # Status Bar
        self.status = ctk.CTkLabel(
            self,
            text="Ready",
            anchor="w"
        )
        self.status.pack(fill="x", padx=10, pady=5)

    def load_examples(self):
        if not self.examples_dir.exists():
            return

        for file in sorted(self.examples_dir.glob("*.poem")):
            btn = ctk.CTkButton(
                self.example_list,
                text=file.name,
                command=lambda f=file: self.load_example(f)
            )
            btn.pack(fill="x", pady=2)

    def load_example(self, file):
        try:
            code = file.read_text(encoding="utf-8")

            self.editor.delete("1.0", "end")
            self.editor.insert("1.0", code)

            self.status.configure(text=f"Loaded {file.name}")

        # FIX: Changed 'catch' to Pythonic 'except'
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run_code(self):
        code = self.editor.get("1.0", "end")
        self.output.delete("1.0", "end")

        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()

            parser = Parser(tokens)
            ast = parser.parse()

            interpreter = Interpreter()
            interpreter.interpret(ast)

            result = "\n".join(
                map(str, interpreter.global_env.get_output())
            )

            self.output.insert("1.0", result)
            self.status.configure(text="Program executed successfully")

        except Exception as e:
            self.output.insert("1.0", f"Error:\n{e}")
            self.status.configure(text="Execution failed")

    def clear_editor(self):
        """Clears both the editor text box and the console output."""
        self.editor.delete("1.0", "end")
        self.output.delete("1.0", "end")
        self.status.configure(text="Cleared editor and console")

    def open_file(self):
        path = filedialog.askopenfilename(
            filetypes=[
                ("Poem Files", "*.poem"),
                ("All Files", "*.*")
            ]
        )
        if not path:
            return

        with open(path, "r", encoding="utf-8") as f:
            self.editor.delete("1.0", "end")
            self.editor.insert("1.0", f.read())
        
        self.status.configure(text=f"Opened {Path(path).name}")

    def save_file(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".poem",
            filetypes=[
                ("Poem Files", "*.poem")
            ]
        )
        if not path:
            return

        with open(path, "w", encoding="utf-8") as f:
            f.write(self.editor.get("1.0", "end"))

        self.status.configure(text="File saved")


if __name__ == "__main__":
    app = PoemScriptStudio()
    app.mainloop()
