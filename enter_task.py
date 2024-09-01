import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime

# Function to add a task
def add_task(event=None):  # Accept event parameter to work with bind
    task = task_entry.get().strip()
    due_date = due_date_entry.get().strip()
    
    # Validate the input
    if not task or not due_date:
        messagebox.showwarning("Input Error", "Both Task and Due Date fields are required.")
        return
    
    try:
        # Try to parse the due date to validate it
        datetime.strptime(due_date, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        messagebox.showwarning("Date Format Error", "Due Date must be in the format 'YYYY-MM-DD HH:MM:SS'.")
        return
    
    # Append the task to the CSV file
    with open('/Users/jerichlee/Documents/aeren/csv/tasks.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([task, due_date])  # Appending data to a new row

    # Clear the entries
    task_entry.delete(0, tk.END)
    due_date_entry.delete(0, tk.END)
    messagebox.showinfo("Success", "Task added successfully!")

# Set up the main window
root = tk.Tk()
root.title("Enter Task")

# Task label and entry
task_label = tk.Label(root, text="Task:")
task_label.pack(pady=5)
task_entry = tk.Entry(root, width=40)
task_entry.pack(pady=5)
task_entry.focus_set()  # Auto-focus on the task entry field

# Due Date label and entry
due_date_label = tk.Label(root, text="Due Date (YYYY-MM-DD HH:MM:SS):")
due_date_label.pack(pady=5)
due_date_entry = tk.Entry(root, width=40)
due_date_entry.pack(pady=5)

# Bind Enter key to the add_task function
root.bind('<Return>', add_task)

# Add Task button
add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.pack(pady=20)

# Run the main loop
root.mainloop()