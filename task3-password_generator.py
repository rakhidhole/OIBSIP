import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip

def generate_password():
    try:
        length = int(length_entry.get())
        charset = ""
        if var_letters.get(): charset += string.ascii_letters
        if var_digits.get(): charset += string.digits
        if var_symbols.get(): charset += string.punctuation
        if not charset:
            raise ValueError("No character types selected.")
        password = ''.join(random.choice(charset) for _ in range(length))
        result_entry.delete(0, tk.END)
        result_entry.insert(0, password)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid input.")

def copy_to_clipboard():
    pyperclip.copy(result_entry.get())
    messagebox.showinfo("Copied", "Password copied to clipboard!")

app = tk.Tk()
app.title("Password Generator")

tk.Label(app, text="Length:").pack()
length_entry = tk.Entry(app)
length_entry.pack()

var_letters = tk.BooleanVar(value=True)
var_digits = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=True)

tk.Checkbutton(app, text="Include Letters", variable=var_letters).pack()
tk.Checkbutton(app, text="Include Digits", variable=var_digits).pack()
tk.Checkbutton(app, text="Include Symbols", variable=var_symbols).pack()

tk.Button(app, text="Generate Password", command=generate_password).pack()

result_entry = tk.Entry(app, width=30)
result_entry.pack()

tk.Button(app, text="Copy to Clipboard", command=copy_to_clipboard).pack()

app.mainloop()
