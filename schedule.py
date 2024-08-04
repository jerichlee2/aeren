import pandas as pd
import tkinter as tk
from tkinter import ttk
from datetime import datetime

# Read the CSV file
file_path = '/Users/jerichlee/Documents/aeren/csv/schedule.csv'
df = pd.read_csv(file_path)

# Get the current day of the week and current time
today_day = datetime.now().strftime('%A')
current_time = datetime.now().time()

# Extract the column for today's day of the week
if today_day in df.columns:
    today_schedule = df[['Time', today_day]]
else:
    print(f"Error: The column for today's day of the week ({today_day}) does not exist in the CSV file.")
    exit()

# Function to convert time string to time object
def str_to_time(time_str):
    try:
        return datetime.strptime(time_str, '%H:%M').time()
    except (ValueError, TypeError):
        return None

# Initialize the tkinter window
root = tk.Tk()
root.title("Schedule")

# Create a treeview to display the schedule
tree = ttk.Treeview(root, columns=('Time', 'Schedule'), show='headings')
tree.pack(expand=True, fill='both')

# Add column headings
tree.heading('Time', text='Time')
tree.heading('Schedule', text='Schedule')

# Variable to track if any cell is highlighted
highlighted = False

# Add rows to the treeview
for index, row in today_schedule.iterrows():
    time_str = row['Time']
    if isinstance(time_str, str):
        time_range = time_str.split('-')
        start_time = str_to_time(time_range[0].strip())
        end_time = str_to_time(time_range[1].strip()) if len(time_range) > 1 else None

        schedule = row[today_day]
        tags = ()

        # Check if current time is within the time range of the current row
        if start_time and (start_time <= current_time < (end_time or (datetime.combine(datetime.today(), start_time) + pd.Timedelta(minutes=30)).time())):
            tags = ('current_time',)
            highlighted = True

        tree.insert("", "end", values=(row['Time'], schedule), tags=tags)

# Highlight the cell for the current time
tree.tag_configure('current_time', background='yellow')

# Run the application
root.mainloop()