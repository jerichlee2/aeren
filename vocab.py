import csv
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

def append_to_csv(file_path, word, definition, context, etymology="", pronunciation=""):
    # Get the current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Create a new row with the provided data in the correct order
    new_row = [word, definition, context, etymology, pronunciation, current_date]
    
    # Append the new row to the CSV file
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(new_row)
    
    # Show a success message
    messagebox.showinfo("Success", "Data saved successfully!")

def submit_entry(event=None):
    word = entry_word.get()
    definition = entry_definition.get()
    context = entry_context.get()
    etymology = entry_etymology.get()
    pronunciation = entry_pronunciation.get()
    
    if not word or not definition or not context:
        messagebox.showwarning("Input Error", "Please fill in all required fields.")
        return
    
    append_to_csv(csv_file_path, word, definition, context, etymology, pronunciation)
    clear_entries()

def clear_entries():
    entry_word.delete(0, tk.END)
    entry_definition.delete(0, tk.END)
    entry_context.delete(0, tk.END)
    entry_etymology.delete(0, tk.END)
    entry_pronunciation.delete(0, tk.END)
    entry_word.focus_set()

# Specify the path to the CSV file
csv_file_path = '/Users/jerichlee/Documents/aeren/csv/vocab.csv'  # Update this with your actual CSV file path

# Create the main window
root = tk.Tk()
root.title("Vocabulary Entry")

# Labels and Entries
label_word = tk.Label(root, text="Word:")
label_word.grid(row=0, column=0, padx=10, pady=10)
entry_word = tk.Entry(root, width=50)
entry_word.grid(row=0, column=1, padx=10, pady=10)

label_definition = tk.Label(root, text="Definition:")
label_definition.grid(row=1, column=0, padx=10, pady=10)
entry_definition = tk.Entry(root, width=50)
entry_definition.grid(row=1, column=1, padx=10, pady=10)

label_context = tk.Label(root, text="Context:")
label_context.grid(row=2, column=0, padx=10, pady=10)
entry_context = tk.Entry(root, width=50)
entry_context.grid(row=2, column=1, padx=10, pady=10)

label_etymology = tk.Label(root, text="Etymology:")
label_etymology.grid(row=3, column=0, padx=10, pady=10)
entry_etymology = tk.Entry(root, width=50)
entry_etymology.grid(row=3, column=1, padx=10, pady=10)

label_pronunciation = tk.Label(root, text="Pronunciation:")
label_pronunciation.grid(row=4, column=0, padx=10, pady=10)
entry_pronunciation = tk.Entry(root, width=50)
entry_pronunciation.grid(row=4, column=1, padx=10, pady=10)

# Save Button
save_button = tk.Button(root, text="Save", command=submit_entry)
save_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Bind the Enter key to the submit_entry function
root.bind('<Return>', submit_entry)

# Set focus to the first entry box when the program starts
entry_word.focus_set()

# Run the Tkinter main loop
root.mainloop()