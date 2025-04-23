import tkinter as tk
from tkinter.colorchooser import askcolor

def pick_color():
    color = askcolor(title="Choose a color")
    if color[1]:
        label.config(text=f"Selected Color: {color[1]}", bg=color[1])

# Create the main application window
root = tk.Tk()
root.title("Color Picker")

# Create a button to open the color picker
button = tk.Button(root, text="Pick a Color", command=pick_color)
button.pack(pady=20)

# Create a label to display the selected color
label = tk.Label(root, text="Selected Color: None", bg="white", width=30, height=2)
label.pack(pady=20)

# Run the application
root.mainloop()