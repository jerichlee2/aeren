import tkinter as tk
from tkinter import ttk
import csv
from datetime import datetime

# Path to the CSV file
csv_file_path = '/Users/jerichlee/Documents/aeren/csv/tasks.csv'

# Function to read tasks from CSV and sort by due date
def read_tasks(csv_file):
    tasks = []
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            task = row['task']
            due_date = datetime.strptime(row['due date'], '%Y-%m-%d %H:%M:%S')
            tasks.append((task, due_date))
    # Sort tasks by due date
    tasks.sort(key=lambda x: x[1])
    return tasks

# Function to display tasks in the Tkinter window
def display_tasks():
    tasks = read_tasks(csv_file_path)
    for task, due_date in tasks:
        tree.insert('', 'end', values=(task, due_date.strftime('%Y-%m-%d %H:%M:%S')))

# Create the main application window
root = tk.Tk()
root.title('Tasks')

# Create a Treeview to display tasks
tree = ttk.Treeview(root, columns=('Task', 'Due Date'), show='headings')
tree.heading('Task', text='Task')
tree.heading('Due Date', text='Due Date')
tree.pack(fill=tk.BOTH, expand=True)

# # Button to refresh tasks
# refresh_button = ttk.Button(root, text="Refresh", command=display_tasks)
# refresh_button.pack(pady=10)

# Load tasks when the application starts
display_tasks()

# Run the Tkinter main loop
root.mainloop()