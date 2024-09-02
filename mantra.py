import tkinter as tk

# Function to read the mantra from the markdown file
def read_mantra(file_path):
    try:
        with open(file_path, 'r') as file:
            mantra = file.read()
        return mantra
    except FileNotFoundError:
        return "Mantra file not found."

# Main function to create the Tkinter window and display the mantra
def display_mantra():
    file_path = "/Users/jerichlee/Documents/aeren/csv/jerich_mantra.md"
    mantra_text = read_mantra(file_path)

    # Create the main window
    root = tk.Tk()
    root.title("Mantra")

    # Specify the font (font family, size)
    custom_font = ("Times New Roman", 14)

    # Create a Text widget to display the mantra
    text_widget = tk.Text(root, wrap=tk.WORD, padx=10, pady=10, font=custom_font)
    text_widget.insert(tk.END, mantra_text)
    text_widget.config(state=tk.DISABLED)  # Make the text read-only
    text_widget.pack(expand=True, fill=tk.BOTH)

    # Run the Tkinter event loop
    root.mainloop()

# Run the application
if __name__ == "__main__":
    display_mantra()