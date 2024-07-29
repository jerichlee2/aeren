import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from food import Food

food_instance = Food()

# def open_file():
#     file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
#     if file_path:
#         try:
#             data = pd.read_csv(file_path)

#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to read file: {e}")

root = tk.Tk()
root.title("My App")

label = tk.Label(root, text="Hello, World!")
label.pack()

# button = tk.Button(root, text="Open CSV and Show Scatter Plot", command=open_file)
# button.pack()
food_instance.create_pie_charts_from_csv('diet_aeren_test.csv')


root.mainloop()