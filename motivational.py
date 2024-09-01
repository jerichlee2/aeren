import tkinter as tk
import csv
from random import choice

# Function to load quotes from the CSV file
def load_quotes(file_path):
    quotes = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            quotes.append({"quote": row[0], "author": row[1]})
    return quotes

# Function to display a random quote
def show_quote():
    quote = choice(quotes)
    quote_label.config(text=f'"{quote["quote"]}"\n\n- {quote["author"]}')

# File path
csv_file_path = '/Users/jerichlee/Documents/aeren/csv/motivational.csv'

# Load quotes from the CSV file
quotes = load_quotes(csv_file_path)

# Create the main window
root = tk.Tk()
root.title("Quote")
root.geometry("400x200")

# Label to display the quote
quote_label = tk.Label(root, text="", wraplength=350, justify="center", font=("Helvetica", 12))
quote_label.pack(pady=20)

# # Button to get a new quote
# new_quote_button = tk.Button(root, text="Show me a quote", command=show_quote)
# new_quote_button.pack()

# Show the first quote
show_quote()

# Run the application
root.mainloop()