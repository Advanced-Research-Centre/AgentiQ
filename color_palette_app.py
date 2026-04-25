import tkinter as tk
from tkinter import colorchooser

def pick_color():
    color_code = colorchooser.askcolor(title="Choose a color")[1]
    if color_code:
        hex_label.config(text=f"Hex Code: {color_code}")

# Create the main application window
root = tk.Tk()
root.title("Color Palette to Hex Code")
root.geometry("300x150")

# Add a button to pick a color
pick_button = tk.Button(root, text="Pick a Color", command=pick_color)
pick_button.pack(pady=20)

# Add a label to display the hex code
hex_label = tk.Label(root, text="Hex Code: None", font=("Arial", 12))
hex_label.pack(pady=10)

# Run the application
root.mainloop()