import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# Initialize SQLite DB
conn = sqlite3.connect('bmi_data.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS bmi_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        weight REAL,
        height REAL,
        bmi REAL,
        category TEXT,
        date TEXT
    )
''')
conn.commit()

# BMI logic
def calculate_bmi(weight, height):
    return weight / (height ** 2)

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

# GUI functionality
def calculate_and_store():
    try:
        name = name_entry.get()
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if weight <= 0 or height <= 0:
            raise ValueError("Inputs must be positive.")

        bmi = calculate_bmi(weight, height)
        category = classify_bmi(bmi)

        result_label.config(text=f"BMI: {bmi:.2f} ({category})")

        # Store in DB
        cursor.execute('''
            INSERT INTO bmi_records (name, weight, height, bmi, category, date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, weight, height, bmi, category, datetime.now().strftime("%Y-%m-%d %H:%M")))
        conn.commit()

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for weight and height.")

def show_history():
    name = name_entry.get()
    if not name:
        messagebox.showerror("Missing Name", "Please enter a name to view history.")
        return

    cursor.execute('SELECT date, bmi FROM bmi_records WHERE name = ?', (name,))
    data = cursor.fetchall()
    if not data:
        messagebox.showinfo("No Data", "No records found for this user.")
        return

    dates, bmis = zip(*data)
    plt.figure(figsize=(8, 4))
    plt.plot(dates, bmis, marker='o')
    plt.xticks(rotation=45)
    plt.title(f'BMI History for {name}')
    plt.xlabel('Date')
    plt.ylabel('BMI')
    plt.tight_layout()
    plt.grid(True)
    plt.show()

# GUI Layout
root = tk.Tk()
root.title("BMI Calculator")

tk.Label(root, text="Name").grid(row=0, column=0, padx=10, pady=5)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)

tk.Label(root, text="Weight (kg)").grid(row=1, column=0, padx=10, pady=5)
weight_entry = tk.Entry(root)
weight_entry.grid(row=1, column=1)

tk.Label(root, text="Height (m)").grid(row=2, column=0, padx=10, pady=5)
height_entry = tk.Entry(root)
height_entry.grid(row=2, column=1)

tk.Button(root, text="Calculate BMI", command=calculate_and_store).grid(row=3, column=0, columnspan=2, pady=10)
tk.Button(root, text="Show History", command=show_history).grid(row=4, column=0, columnspan=2)

result_label = tk.Label(root, text="", font=("Helvetica", 12))
result_label.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()
