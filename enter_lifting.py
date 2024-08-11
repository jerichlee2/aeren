import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime

# Path to your CSV file
csv_file_path = '/Users/jerichlee/Documents/aeren/csv/lifting.csv'

# Function to append data to the next empty row in the CSV file
def append_to_csv(lift_type, active_zone_minutes):
    current_date = datetime.now().strftime('%m/%d/%y')
    
    # Read the existing rows
    with open(csv_file_path, mode='r', newline='') as file:
        reader = list(csv.reader(file))

    # Find the first fully empty row
    found_empty_row = False
    for row in reader:
        if all(cell == '' for cell in row):  # Check if all cells in the row are empty
            row[0] = lift_type
            row[6] = active_zone_minutes
            row[7] = current_date
            found_empty_row = True
            break
    
    # If no fully empty row is found, append a new row
    if not found_empty_row:
        reader.append([lift_type, "", "", "", "", "", active_zone_minutes, current_date, ""])
    
    # Write the updated data back to the CSV file
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(reader)
    
    messagebox.showinfo("Success", "Data added to CSV!")

# Function to handle the submit action
def on_submit():
    lift_type = lift_type_var.get()
    active_zone_minutes = active_zone_minutes_var.get()

    if not lift_type or not active_zone_minutes:
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        active_zone_minutes = int(active_zone_minutes)
    except ValueError:
        messagebox.showerror("Error", "Active Zone Minutes must be a number!")
        return

    append_to_csv(lift_type, active_zone_minutes)
    lift_type_var.set("")
    active_zone_minutes_var.set("")
    lift_type_entry.focus()
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("Add Lifting Data")

# Variables to hold input data
lift_type_var = tk.StringVar()
active_zone_minutes_var = tk.StringVar()

# Lift Type Label and Entry
lift_type_label = tk.Label(root, text="Type of Lift:")
lift_type_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
lift_type_entry = tk.Entry(root, textvariable=lift_type_var)
lift_type_entry.grid(row=0, column=1, padx=10, pady=5)
lift_type_entry.focus()

# Active Zone Minutes Label and Entry
active_zone_minutes_label = tk.Label(root, text="Total Active Zone Minutes:")
active_zone_minutes_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
active_zone_minutes_entry = tk.Entry(root, textvariable=active_zone_minutes_var)
active_zone_minutes_entry.grid(row=1, column=1, padx=10, pady=5)

# Submit Button
submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.grid(row=2, columnspan=2, pady=10)

# Bind Enter key to the submit function so you can press Enter to submit
root.bind('<Return>', lambda event: on_submit())

# Run the application
root.mainloop()