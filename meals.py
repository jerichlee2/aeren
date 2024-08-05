import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import datetime

# Ensure the CSV directory exists
if not os.path.exists('csv'):
    os.makedirs('csv')

# Function to read CSV and return list of rows
def read_csv(file):
    if not os.path.exists(file):
        return []
    with open(file, mode='r', newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)

# Function to write to CSV
def write_csv(file, rows, mode='a'):
    file_exists = os.path.exists(file)
    with open(file, mode=mode, newline='') as f:
        fieldnames = ['Meal', 'Name', 'Food Item', 'Calories', 'Carbs (g)', 'Protein (g)', 'Fat (g)', 'Date Added']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists or os.path.getsize(file) == 0:
            writer.writeheader()
        writer.writerows(rows)

# Function to search for name in csv/meals.csv
def search_name(name):
    meals = read_csv('csv/meals.csv')
    for row in meals:
        if row['Name'].lower() == name.lower():
            return row
    return None

# Function to add meal to csv/meals.csv
def add_meal(meal_data):
    write_csv('csv/meals.csv', [meal_data], mode='a')

# Function to append meal to csv/diet.csv with the current date
def append_to_diet_log(meal_data):
    # Ensure only relevant fields are included
    meal_data_copy = {k: meal_data[k] for k in ['Meal', 'Name', 'Food Item', 'Calories', 'Carbs (g)', 'Protein (g)', 'Fat (g)']}
    meal_data_copy['Date Added'] = datetime.now().strftime('%Y-%m-%d')
    write_csv('csv/diet.csv', [meal_data_copy], mode='a')

# Function to handle user input
def handle_input(event=None):
    name = entry.get()
    if not name:
        messagebox.showerror("Error", "Name cannot be empty.")
        return
    
    meal_data = search_name(name)
    
    if meal_data:
        append_to_diet_log(meal_data)
        messagebox.showinfo("Success", f"{name} has been added to csv/diet.csv.")
        root.destroy()  # Exit the program
    else:
        if messagebox.askyesno("Meal not found", f"{name} not found. Do you want to add it to csv/meals.csv?"):
            add_new_meal(name)

# Function to add a new meal to csv/meals.csv
def add_new_meal(name):
    new_meal_window = tk.Toplevel(root)
    new_meal_window.title("Add New Meal")
    
    tk.Label(new_meal_window, text="Meal:").grid(row=0, column=0, padx=10, pady=10)
    tk.Label(new_meal_window, text="Name:").grid(row=1, column=0, padx=10, pady=10)
    tk.Label(new_meal_window, text="Food Item:").grid(row=2, column=0, padx=10, pady=10)
    tk.Label(new_meal_window, text="Calories:").grid(row=3, column=0, padx=10, pady=10)
    tk.Label(new_meal_window, text="Carbs (g):").grid(row=4, column=0, padx=10, pady=10)
    tk.Label(new_meal_window, text="Protein (g):").grid(row=5, column=0, padx=10, pady=10)
    tk.Label(new_meal_window, text="Fat (g):").grid(row=6, column=0, padx=10, pady=10)
    
    entry_meal = tk.Entry(new_meal_window)
    entry_name = tk.Entry(new_meal_window)
    entry_food_item = tk.Entry(new_meal_window)
    entry_calories = tk.Entry(new_meal_window)
    entry_carbs = tk.Entry(new_meal_window)
    entry_protein = tk.Entry(new_meal_window)
    entry_fat = tk.Entry(new_meal_window)
    
    entry_meal.grid(row=0, column=1, padx=10, pady=10)
    entry_name.grid(row=1, column=1, padx=10, pady=10)
    entry_food_item.grid(row=2, column=1, padx=10, pady=10)
    entry_calories.grid(row=3, column=1, padx=10, pady=10)
    entry_carbs.grid(row=4, column=1, padx=10, pady=10)
    entry_protein.grid(row=5, column=1, padx=10, pady=10)
    entry_fat.grid(row=6, column=1, padx=10, pady=10)
    
    entry_name.insert(0, name)
    entry_meal.focus_set()  # Set focus to the first entry widget
    
    def save_new_meal(event=None):
        date_added = datetime.now().strftime('%Y-%m-%d')
        meal_data = {
            'Meal': entry_meal.get(),
            'Name': entry_name.get(),
            'Food Item': entry_food_item.get(),
            'Calories': entry_calories.get(),
            'Carbs (g)': entry_carbs.get(),
            'Protein (g)': entry_protein.get(),
            'Fat (g)': entry_fat.get(),
            'Date Added': date_added
        }
        add_meal(meal_data)
        messagebox.showinfo("Success", f"{entry_name.get()} has been added to csv/meals.csv.")
        new_meal_window.destroy()
    
    save_button = tk.Button(new_meal_window, text="Save", command=save_new_meal)
    save_button.grid(row=7, column=0, columnspan=2, pady=10)
    
    # Bind the Enter key to the save_new_meal function
    new_meal_window.bind('<Return>', save_new_meal)

# Create main window
root = tk.Tk()
root.title("Diet Log")

tk.Label(root, text="Enter name:").pack(pady=10)
entry = tk.Entry(root)
entry.pack(pady=5)
entry.focus_set()  # Set focus to the entry widget

add_button = tk.Button(root, text="Add Meal", command=handle_input)
add_button.pack(pady=10)

# Bind the Enter key to the handle_input function
root.bind('<Return>', handle_input)

root.mainloop()