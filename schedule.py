import pandas as pd
import tkinter as tk
from tkinter import ttk
from datetime import datetime

# Read the CSV file
file_path = '/Users/jerichlee/Documents/aeren/csv/schedule.csv'
df = pd.read_csv(file_path)

# Initialize the tkinter window
root = tk.Tk()
root.title("Schedule")

# Create a treeview to display the schedule
tree = ttk.Treeview(root, columns=('Time', 'Schedule'), show='headings')
tree.pack(expand=True, fill='both')

# Add column headings
tree.heading('Time', text='Time')
tree.heading('Schedule', text='Schedule')

# Function to convert time string to time object
def str_to_time(time_str):
    try:
        return datetime.strptime(time_str, '%H:%M').time()
    except (ValueError, TypeError):
        return None

# Function to update the schedule based on the selected day
def update_schedule(selected_day):
    global highlighted
    highlighted = False
    # Clear the current content of the treeview
    for item in tree.get_children():
        tree.delete(item)
    
    # Check if the selected day exists in the dataframe
    if selected_day in df.columns:
        day_schedule = df[['Time', selected_day]]
        current_time = datetime.now().time()

        # Add rows to the treeview for the selected day
        for index, row in day_schedule.iterrows():
            time_str = row['Time']
            if isinstance(time_str, str):
                time_range = time_str.split('-')
                start_time = str_to_time(time_range[0].strip())
                end_time = str_to_time(time_range[1].strip()) if len(time_range) > 1 else None

                schedule = row[selected_day]
                tags = ()

                # Check if current time is within the time range of the current row
                if start_time and (start_time <= current_time < (end_time or (datetime.combine(datetime.today(), start_time) + pd.Timedelta(minutes=30)).time())):
                    tags = ('current_time',)
                    highlighted = True

                tree.insert("", "end", values=(row['Time'], schedule), tags=tags)

        # Highlight the cell for the current time
        tree.tag_configure('current_time', background='yellow')
        
        # Update the day label
        day_label.config(text=f"{selected_day}")
    else:
        print(f"Error: The column for the selected day ({selected_day}) does not exist in the CSV file.")

# Variables to track the current day
current_day_index = datetime.now().weekday()  # Monday is 0, Sunday is 6
days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Function to go to the next day
def next_day():
    global current_day_index
    current_day_index = (current_day_index + 1) % 7
    update_schedule(days_of_week[current_day_index])

# Function to go to the previous day
def previous_day():
    global current_day_index
    current_day_index = (current_day_index - 1) % 7
    update_schedule(days_of_week[current_day_index])

# Function to reset to the current day
def reset_to_today():
    global current_day_index
    current_day_index = datetime.now().weekday()
    update_schedule(days_of_week[current_day_index])

# Create a label to display the current day
day_label = tk.Label(root, text="")
day_label.pack(pady=10)

# Create buttons to navigate days
prev_button = tk.Button(root, text="Prev", command=previous_day)
prev_button.pack(side='left', padx=10, pady=10)

next_button = tk.Button(root, text="Next", command=next_day)
next_button.pack(side='right', padx=10, pady=10)

# Create a reset button to go back to the current day
reset_button = tk.Button(root, text="Reset", command=reset_to_today)
reset_button.pack(pady=10)

# Initial load of today's schedule
today_day = days_of_week[current_day_index]
update_schedule(today_day)

# Run the application
root.mainloop()