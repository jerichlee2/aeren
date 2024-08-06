import csv
import os
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox

def update_last_entry_in_csv(file_path, comments):
    # Get the current time
    current_time = datetime.now().strftime('%I:%M %p')
    
    # Read the existing content of the CSV file
    rows = []
    file_exists = os.path.isfile(file_path)
    if file_exists:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)
    
    # Check if there are any rows to update
    if not rows or len(rows) < 2:
        messagebox.showwarning("Input Error", "No existing entry to update.")
        return
    
    # Update the last row with the current time and comments
    last_row = rows[-1]
    if not any(last_row):
        messagebox.showwarning("Input Error", "Last row is empty, cannot update.")
        return
    
    # Ensure the 'End Time' and 'Comments' columns are correct
    if len(last_row) < 6:
        last_row.extend([''] * (6 - len(last_row)))
    
    last_row[2] = current_time
    last_row[4] = comments
    
    # Calculate the total duration read, rounding to the nearest half hour
    try:
        start_time = datetime.strptime(last_row[1], '%I:%M %p')
        end_time = datetime.strptime(last_row[2], '%I:%M %p')
        # Handle PM to AM transition
        if start_time > end_time:
            end_time += timedelta(days=1)
        duration = end_time - start_time
        duration_hours = duration.total_seconds() / 3600
        duration_rounded = round(duration_hours * 2) / 2  # Round to the nearest half hour
        last_row[5] = duration_rounded
    except Exception as e:
        messagebox.showerror("Error", f"Error calculating duration: {e}")
        return
    
    # Write the rows back to the CSV file
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def submit_entry(event=None):
    comments = entry_comments.get()
    if not comments:
        messagebox.showwarning("Input Error", "Please enter your comments.")
        return
    update_last_entry_in_csv(csv_file_path, comments)
    root.destroy()

# Specify the path to the CSV file
csv_file_path = '/Users/jerichlee/Documents/aeren/csv/books.csv'  # Update this with your actual CSV file path

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