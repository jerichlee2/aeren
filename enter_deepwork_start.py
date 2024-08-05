import csv
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

def add_entry_to_csv(file_path, goals):
    # Get the current date and time
    current_date = datetime.now().strftime('%m/%d/%y')
    current_time = datetime.now().strftime('%I:%M %p')
    
    # Read the existing content of the CSV file
    rows = []
    file_exists = os.path.isfile(file_path)
    if file_exists:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)
    
    # Remove any empty rows from the end
    while rows and not any(rows[-1]):
        rows.pop()
    
    # Add the new entry to the rows list
    rows.append([current_date, current_time, '', goals, ''])
    
    # Write the rows back to the CSV file
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header if the file did not exist
        if not file_exists:
            writer.writerow(['Date', 'Start Time', 'End Time', 'Goals', 'Comments'])
        
        # Write all rows including the new entry
        writer.writerows(rows)        

def submit_entry(event=None):
    goals = entry_goals.get()
    if not goals:
        messagebox.showwarning("Input Error", "Please enter your goals.")
        return
    add_entry_to_csv(csv_file_path, goals)
    root.destroy()

# Specify the path to the CSV file
csv_file_path = '/Users/jerichlee/Documents/aeren/csv/deepwork.csv'  # Update this with your actual CSV file path

# Create the main window
root = tk.Tk()
root.title("Enter Deepwork Start")

# Create and place the widgets
label_goals = tk.Label(root, text="Goals:")
label_goals.grid(row=0, column=0, padx=10, pady=5, sticky='e')
entry_goals = tk.Entry(root, width=50)
entry_goals.grid(row=0, column=1, padx=10, pady=5)
entry_goals.focus_set()

button_submit = tk.Button(root, text="Submit", command=submit_entry)
button_submit.grid(row=1, column=0, columnspan=2, pady=10)

# Bind the Enter key to the submit_entry function
root.bind('<Return>', submit_entry)

# Run the application
root.mainloop()