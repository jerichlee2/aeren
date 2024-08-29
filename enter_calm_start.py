import csv
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

def add_entry_to_csv(file_path):
    # Get the current date and time
    current_date = datetime.now().strftime('%Y-%m-%d')
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
    rows.append([current_date, current_time, ''])
    
    # Write the rows back to the CSV file
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header if the file did not exist
        if not file_exists:
            writer.writerow(['Date', 'Start Time', 'End Time'])
        
        # Write all rows including the new entry
        writer.writerows(rows)        

def submit_entry(event=None):
    add_entry_to_csv(csv_file_path)
    root.destroy()

# Specify the path to the CSV file
csv_file_path = '/Users/jerichlee/Documents/aeren/csv/calm.csv'  # Update this with your actual CSV file path

# Create the main window
root = tk.Tk()
root.title("Enter Calm Start")

button_submit = tk.Button(root, text="Submit", command=submit_entry)
button_submit.grid(row=1, column=0, columnspan=2, pady=10)

# Bind the Enter key to the submit_entry function
root.bind('<Return>', submit_entry)

# Run the application
root.mainloop()