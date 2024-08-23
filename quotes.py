import csv
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

def append_to_csv(file_path, quote, author):
    # Get the current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Create a new row with the provided data in the correct order
    new_row = [quote, author, current_date]
    
    # Append the new row to the CSV file
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(new_row)
    
    # Show a success message
    messagebox.showinfo("Success", "Quote saved successfully!")

def submit_entry(event=None):
    quote = entry_quote.get()
    author = entry_author.get()
    
    if not quote or not author:
        messagebox.showwarning("Input Error", "Please fill in all required fields.")
        return
    
    append_to_csv(csv_file_path, quote, author)
    clear_entries()

def clear_entries():
    entry_quote.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_quote.focus_set()

# Specify the path to the CSV file
csv_file_path = '/Users/jerichlee/Documents/aeren/csv/quotes.csv'  # Update this with your actual CSV file path

# Create the main window
root = tk.Tk()
root.title("Quote Entry")

# Labels and Entries
label_quote = tk.Label(root, text="Quote:")
label_quote.grid(row=0, column=0, padx=10, pady=10)
entry_quote = tk.Entry(root, width=50)
entry_quote.grid(row=0, column=1, padx=10, pady=10)

label_author = tk.Label(root, text="Author:")
label_author.grid(row=1, column=0, padx=10, pady=10)
entry_author = tk.Entry(root, width=50)
entry_author.grid(row=1, column=1, padx=10, pady=10)

# Save Button
save_button = tk.Button(root, text="Save", command=submit_entry)
save_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Bind the Enter key to the submit_entry function
root.bind('<Return>', submit_entry)

# Set focus to the first entry box when the program starts
entry_quote.focus_set()

# Run the Tkinter main loop
root.mainloop()