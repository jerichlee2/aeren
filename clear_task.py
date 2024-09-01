import tkinter as tk
from tkinter import messagebox
import csv

# Function to clear a task
def clear_task(event=None):  # Accept event parameter to work with bind
    task_to_clear = task_entry.get().strip()
    
    # Validate the input
    if not task_to_clear:
        messagebox.showwarning("Input Error", "Task field cannot be empty.")
        return
    
    # Read the current tasks from the CSV file
    tasks = []
    file_path = '/Users/jerichlee/Documents/aeren/csv/tasks.csv'
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        tasks = [row for row in reader if row]  # Read all tasks into a list
    
    # Filter out the task to be cleared
    tasks_after_clear = [task for task in tasks if task[0] != task_to_clear]
    
    # If the task was not found, show a message
    if len(tasks) == len(tasks_after_clear):
        messagebox.showwarning("Task Not Found", "The specified task was not found.")
        return
    
    # Write the updated task list back to the CSV file
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(tasks_after_clear)
    
    # Clear the entry
    task_entry.delete(0, tk.END)
    messagebox.showinfo("Success", "Task cleared successfully!")

# Set up the main window
root = tk.Tk()
root.title("Complete Task")

# Task label and entry
task_label = tk.Label(root, text="Task to clear:")
task_label.pack(pady=5)
task_entry = tk.Entry(root, width=40)
task_entry.pack(pady=5)
task_entry.focus_set()  # Auto-focus on the task entry field

# Bind Enter key to the clear_task function
root.bind('<Return>', clear_task)

# Clear Task button
clear_button = tk.Button(root, text="Clear Task", command=clear_task)
clear_button.pack(pady=20)

# Run the main loop
root.mainloop()