import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

class CSVAggregatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Aggregator")

        self.deepwork_file = "/Users/jerichlee/Documents/aeren/csv/deepwork.csv"
        self.books_file = "/Users/jerichlee/Documents/aeren/csv/books.csv"
        self.diet_file = "/Users/jerichlee/Documents/aeren/csv/diet.csv"
        self.schedule_file = "/Users/jerichlee/Documents/aeren/csv/schedule.csv"

        # Create and place buttons
        self.create_widgets()

    def create_widgets(self):
        self.load_deepwork_button = tk.Button(self.root, text="Load Deepwork CSV", command=self.load_deepwork)
        self.load_deepwork_button.grid(row=0, column=0, padx=10, pady=10)

        self.load_books_button = tk.Button(self.root, text="Load Books CSV", command=self.load_books)
        self.load_books_button.grid(row=0, column=1, padx=10, pady=10)

        self.load_diet_button = tk.Button(self.root, text="Load Diet CSV", command=self.load_diet)
        self.load_diet_button.grid(row=0, column=2, padx=10, pady=10)

        self.load_schedule_button = tk.Button(self.root, text="Load Schedule CSV", command=self.load_schedule)
        self.load_schedule_button.grid(row=0, column=3, padx=10, pady=10)

        self.aggregate_button = tk.Button(self.root, text="Aggregate Data", command=self.aggregate_data)
        self.aggregate_button.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

    def load_deepwork(self):
        self.deepwork_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.deepwork_file:
            messagebox.showinfo("Loaded", f"Loaded Deepwork CSV: {self.deepwork_file}")

    def load_books(self):
        self.books_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.books_file:
            messagebox.showinfo("Loaded", f"Loaded Books CSV: {self.books_file}")

    def load_diet(self):
        self.diet_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.diet_file:
            messagebox.showinfo("Loaded", f"Loaded Diet CSV: {self.diet_file}")

    def load_schedule(self):
        self.schedule_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.schedule_file:
            messagebox.showinfo("Loaded", f"Loaded Schedule CSV: {self.schedule_file}")

    def aggregate_data(self):
        if not (self.deepwork_file and self.books_file and self.diet_file and self.schedule_file):
            messagebox.showwarning("Error", "Please load all CSV files before aggregating.")
            return

        # Load the data from the CSV files
        deepwork_df = pd.read_csv(self.deepwork_file)
        books_df = pd.read_csv(self.books_file)
        diet_df = pd.read_csv(self.diet_file)
        schedule_df = pd.read_csv(self.schedule_file)

        # Here we just concatenate the dataframes for simplicity
        # You can modify this part to process/aggregate the data as needed
        combined_df = pd.concat([deepwork_df, books_df, diet_df, schedule_df], ignore_index=True)

        # Save the combined data to the aggre.csv file
        combined_df.to_csv('aggre.csv', index=False)
        messagebox.showinfo("Success", "Data aggregated and saved to aggre.csv")

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVAggregatorApp(root)
    root.mainloop()