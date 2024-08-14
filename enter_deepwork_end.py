import csv
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

def update_last_entry_in_csv(file_path, comments):
    # Get the current date and time
    current_time = datetime.now().strftime('%I:%M %p')
    
    # Read the existing content of the CSV file
    rows = []
    file_exists = os.path.isfile(file_path)
    if file_exists:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                # Ensure each row has exactly 6 fields
                if len(row) < 6:
                    row.extend([''] * (6 - len(row)))
                elif len(row) > 6:
                    row = row[:6]
                rows.append(row)
    
    # Check if there are any rows to update
    if not rows or len(rows) < 2:
        messagebox.showwarning("Input Error", "No existing entry to update.")
        return
    
    # Update the last row with the current date, time, and comments
    last_row = rows[-1]
    if not any(last_row):
        messagebox.showwarning("Input Error", "Last row is empty, cannot update.")
        return
    
    last_row[2] = current_time  # Assuming the third column is 'End Time'
    last_row[4] = comments      # Assuming the fifth column is 'Comments'
    
    # Save the updated rows back to the CSV file
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    
    # Show a message that the entry was successfully updated

def submit_entry(event=None):
    comments = entry_comments.get()
    if not comments:
        messagebox.showwarning("Input Error", "Please enter your comments.")
        return
    update_last_entry_in_csv(csv_file_path, comments)
    root.destroy()

# Specify the path to the CSV file
csv_file_path = '/Users/jerichlee/Documents/aeren/csv/deepwork.csv'  # Update this with your actual CSV file path

# Create the main window
root = tk.Tk()
root.title("Enter Reading End")

# Create and place the widgets
label_comments = tk.Label(root, text="Comments:")
label_comments.grid(row=0, column=0, padx=10, pady=5, sticky='e')
entry_comments = tk.Entry(root, width=50)
entry_comments.grid(row=0, column=1, padx=10, pady=5)
entry_comments.focus_set()

button_submit = tk.Button(root, text="Submit", command=submit_entry)
button_submit.grid(row=1, column=0, columnspan=2, pady=10)

# Bind the Enter key to the submit_entry function
root.bind('<Return>', submit_entry)

# Run the application
root.mainloop()