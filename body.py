import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime

def calculate_average(values):
    return sum(values) / len(values)

def calculate_body_fat(chest_avg, abdomen_avg, thigh_avg, age, gender="male"):
    # Sum of the skinfolds
    sum_skinfolds = chest_avg + abdomen_avg + thigh_avg
    
    # Calculate body density using the Jackson/Pollock 3-site formula
    if gender == "male":
        body_density = 1.10938 - (0.0008267 * sum_skinfolds) + (0.0000016 * (sum_skinfolds ** 2)) - (0.0002574 * age)
    else:
        body_density = 1.0994921 - (0.0009929 * sum_skinfolds) + (0.0000023 * (sum_skinfolds ** 2)) - (0.0001392 * age)
    
    # Convert body density to body fat percentage using the Siri equation
    body_fat_percentage = (495 / body_density) - 450
    
    return body_fat_percentage

def clean_csv(file_name):
    lines = []
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            cleaned_row = [item.strip() for item in row if item.strip()]
            if cleaned_row:  # Only append rows that have data
                lines.append(cleaned_row)
    
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(lines)

def save_to_csv(date, body_fat_percentage, body_weight):
    clean_csv('/Users/jerichlee/Documents/aeren/csv/body.csv')  # Clean the CSV before appending
    with open('/Users/jerichlee/Documents/aeren/csv/body.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, f"{body_fat_percentage:.2f}", body_weight])

def submit(event=None):
    try:
        chest_values = [float(chest1.get()), float(chest2.get()), float(chest3.get())]
        abdomen_values = [float(abdomen1.get()), float(abdomen2.get()), float(abdomen3.get())]
        thigh_values = [float(thigh1.get()), float(thigh2.get()), float(thigh3.get())]
        global age
        age = int(age_entry.get())
        body_weight = float(weight_entry.get())

        chest_avg = calculate_average(chest_values)
        abdomen_avg = calculate_average(abdomen_values)
        thigh_avg = calculate_average(thigh_values)

        body_fat_percentage = calculate_body_fat(chest_avg, abdomen_avg, thigh_avg, age, gender="male")  # Use "female" if needed
        
        today_date = datetime.today().strftime('%Y-%m-%d')
        
        save_to_csv(today_date, body_fat_percentage, body_weight)
        
        messagebox.showinfo("Success", f"Body fat percentage: {body_fat_percentage:.2f}% and weight: {body_weight} have been saved to body.csv")
        root.destroy()
    except ValueError:
        messagebox.showerror("Input Error", "Please ensure all inputs are numeric.")
        root.destroy()

# Tkinter GUI
root = tk.Tk()
root.title("Body Fat Percentage Calculator")

tk.Label(root, text="Enter age:").grid(row=0, column=0)
age_entry = tk.Entry(root)
age_entry.grid(row=0, column=1)
age_entry.focus()  # Set focus on the age entry field

tk.Label(root, text="Chest Measurement 1:").grid(row=1, column=0)
chest1 = tk.Entry(root)
chest1.grid(row=1, column=1)

tk.Label(root, text="Chest Measurement 2:").grid(row=2, column=0)
chest2 = tk.Entry(root)
chest2.grid(row=2, column=1)

tk.Label(root, text="Chest Measurement 3:").grid(row=3, column=0)
chest3 = tk.Entry(root)
chest3.grid(row=3, column=1)

tk.Label(root, text="Abdomen Measurement 1:").grid(row=4, column=0)
abdomen1 = tk.Entry(root)
abdomen1.grid(row=4, column=1)

tk.Label(root, text="Abdomen Measurement 2:").grid(row=5, column=0)
abdomen2 = tk.Entry(root)
abdomen2.grid(row=5, column=1)

tk.Label(root, text="Abdomen Measurement 3:").grid(row=6, column=0)
abdomen3 = tk.Entry(root)
abdomen3.grid(row=6, column=1)

tk.Label(root, text="Thigh Measurement 1:").grid(row=7, column=0)
thigh1 = tk.Entry(root)
thigh1.grid(row=7, column=1)

tk.Label(root, text="Thigh Measurement 2:").grid(row=8, column=0)
thigh2 = tk.Entry(root)
thigh2.grid(row=8, column=1)

tk.Label(root, text="Thigh Measurement 3:").grid(row=9, column=0)
thigh3 = tk.Entry(root)
thigh3.grid(row=9, column=1)

tk.Label(root, text="Enter Body Weight:").grid(row=10, column=0)
weight_entry = tk.Entry(root)
weight_entry.grid(row=10, column=1)

submit_btn = tk.Button(root, text="Calculate and Save", command=submit)
submit_btn.grid(row=11, column=0, columnspan=2)

# Bind the Enter key to the submit function
root.bind('<Return>', submit)

root.mainloop()