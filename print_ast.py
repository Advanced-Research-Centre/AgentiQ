import ast
import astpretty
import tkinter as tk
from tkinter import scrolledtext

def display_ast(file_path):
    try:
        with open(file_path, 'r') as source_file:
            source_code = source_file.read()

        # Parse the source code into an AST
        tree = ast.parse(source_code)

        # Create a Tkinter window
        root = tk.Tk()
        root.title("Abstract Syntax Tree Viewer")

        # Create a scrolled text widget to display the AST
        text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=40)
        text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Pretty print the AST into the text widget
        pretty_ast = astpretty.pformat(tree)
        text_area.insert(tk.END, pretty_ast)

        # Run the Tkinter main loop
        root.mainloop()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python print_ast.py <source_file.py>")
    else:
        display_ast(sys.argv[1])