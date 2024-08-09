import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
from datetime import datetime, timedelta

class DietApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aggregator")
        
        # Create a frame for the data display
        self.frame = tk.Frame(root)
        self.frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        # Create a Treeview widget
        self.tree = ttk.Treeview(self.frame, columns=("Stat", "Value"), show='headings')
        self.tree.heading("Stat", text="Stat")
        self.tree.heading("Value", text="Value")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add a vertical scrollbar
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        # Process the CSV files upon initialization
        self.process_csv()

    def process_csv(self):
        diet_file_path = '/Users/jerichlee/Documents/aeren/csv/diet.csv'
        books_file_path = '/Users/jerichlee/Documents/aeren/csv/books.csv'
        deepwork_file_path = '/Users/jerichlee/Documents/aeren/csv/deepwork.csv'
        
        if not os.path.exists(diet_file_path) or not os.path.exists(books_file_path) or not os.path.exists(deepwork_file_path):
            messagebox.showerror("Error", "File not found!")
            return
        
        # Read the diet CSV file
        diet_df = pd.read_csv(diet_file_path)
        
        # Focus on the specified columns
        diet_df = diet_df[['Calories', 'Carbs (g)', 'Protein (g)', 'Fat (g)', 'Date']]
        
        # Convert Date column to datetime with specified format
        diet_df['Date'] = pd.to_datetime(diet_df['Date'], format='%m/%d/%y')
        
        # Get today's date
        today_date = pd.to_datetime(datetime.now().strftime('%m/%d/%y'))
        
        # Filter the diet data to include only the last 7 days
        last_week = today_date - timedelta(days=6)
        date_range = pd.date_range(last_week, today_date)
        diet_df_last_week = diet_df[diet_df['Date'].isin(date_range)]
        
        # Group by Date and calculate daily sums for the last 7 days
        daily_sums_last_week = diet_df_last_week.groupby('Date').sum().reindex(date_range, fill_value=0)
        
        # Compute the mean of the last 7 days and convert to two decimal places
        mean_values_last_week = daily_sums_last_week.mean().round(2).to_dict()
        
        # Filter today's values and convert to two decimal places
        if today_date in daily_sums_last_week.index:
            today_values = daily_sums_last_week.loc[today_date].round(2).to_dict()
        else:
            today_values = {
                'Calories': 0.0,
                'Carbs (g)': 0.0,
                'Protein (g)': 0.0,
                'Fat (g)': 0.0
            }
        
        # Debugging: Print values for diet (food)
        print("Total Calories (Last 7 Days):", daily_sums_last_week['Calories'].sum())
        print("Daily Calories:", daily_sums_last_week['Calories'])
        print("Mean Calories Per Day (Last 7 Days):", mean_values_last_week['Calories'])
        
        # Read the books CSV file
        books_df = pd.read_csv(books_file_path)
        
        # Convert Date column to datetime with specified format
        books_df['Date'] = pd.to_datetime(books_df['Date'], format='%Y-%m-%d')
        
        # Calculate duration for each reading session
        books_df['Start Time'] = pd.to_datetime(books_df['Start Time'], format='%I:%M %p', errors='coerce')
        books_df['End Time'] = pd.to_datetime(books_df['End Time'], format='%I:%M %p', errors='coerce')
        books_df['Duration'] = (books_df['End Time'] - books_df['Start Time']).dt.total_seconds() / 3600
        
        # Filter the books data to include only the last 7 days
        books_df_last_week = books_df[(books_df['Date'] >= last_week) & (books_df['Date'] <= today_date)]
        
        # Create a DataFrame with the last 7 days, filling missing dates with 0
        daily_reading_time = books_df_last_week.groupby('Date')['Duration'].sum().reindex(date_range, fill_value=0)
        
        # Calculate the total and weekly average reading time (Duration) for the last 7 days including zeros
        total_reading_time_last_week = daily_reading_time.sum()
        weekly_avg_reading_time = (total_reading_time_last_week / 7).round(3)  # Divide by 7 to include all days
        
        # Debugging: Print values for reading
        print("Total Reading Time (Last 7 Days):", total_reading_time_last_week)
        print("Daily Reading Times:", daily_reading_time)
        print("Weekly Average Reading Time:", weekly_avg_reading_time)
        
        # Get today's reading time
        today_reading_time = daily_reading_time.loc[today_date]
        
        # Read the deep work CSV file
        deepwork_df = pd.read_csv(deepwork_file_path)
        
        # Convert Date column to datetime
        deepwork_df['Date'] = pd.to_datetime(deepwork_df['Date'], format='%m/%d/%y')
        
        # Calculate duration for each deep work session
        deepwork_df['Start Time'] = pd.to_datetime(deepwork_df['Start Time'], format='%I:%M %p')
        deepwork_df['End Time'] = pd.to_datetime(deepwork_df['End Time'], format='%I:%M %p')
        deepwork_df['Duration'] = (deepwork_df['End Time'] - deepwork_df['Start Time']).dt.total_seconds() / 3600
        
        # Filter the deep work data to include only the last 7 days
        deepwork_df_last_week = deepwork_df[(deepwork_df['Date'] >= last_week) & (deepwork_df['Date'] <= today_date)]
        
        # Create a DataFrame with the last 7 days, filling missing dates with 0
        daily_deepwork_time = deepwork_df_last_week.groupby('Date')['Duration'].sum().reindex(date_range, fill_value=0)
        
        # Calculate the total and weekly average deep work duration for the last 7 days including zeros
        total_deepwork_time_last_week = daily_deepwork_time.sum()
        weekly_avg_deepwork_time = (total_deepwork_time_last_week / 7).round(3)
        
        # Debugging: Print values for deep work
        print("Total Deep Work Time (Last 7 Days):", total_deepwork_time_last_week)
        print("Daily Deep Work Times:", daily_deepwork_time)
        print("Weekly Average Deep Work Time:", weekly_avg_deepwork_time)
        
        # Get today's deep work duration
        today_deepwork_time = daily_deepwork_time.loc[today_date]
        
        # Prepare the data to append
        mean_data = {
            'Stat': [
                'Mean Calories/Day (Last 7 Days)',
                'Mean Carbs (g)/Day (Last 7 Days)',
                'Mean Protein (g)/Day (Last 7 Days)',
                'Mean Fat (g)/Day (Last 7 Days)',
                'Weekly Average Time Reading (Hours)',
                'Weekly Average Deep Work Time (Hours)',
                "Today's Calories",
                "Today's Carbs (g)",
                "Today's Protein (g)",
                "Today's Fat (g)",
                "Today's Time Reading (Hours)",
                "Today's Deep Work Time (Hours)"
            ],
            'Value': [
                mean_values_last_week.get('Calories', 0.0),
                mean_values_last_week.get('Carbs (g)', 0.0),
                mean_values_last_week.get('Protein (g)', 0.0),
                mean_values_last_week.get('Fat (g)', 0.0),
                weekly_avg_reading_time,
                weekly_avg_deepwork_time,
                today_values.get('Calories', 0.0),
                today_values.get('Carbs (g)', 0.0),
                today_values.get('Protein (g)', 0.0),
                today_values.get('Fat (g)', 0.0),
                today_reading_time,
                today_deepwork_time
            ]
        }
        
        mean_df = pd.DataFrame(mean_data)
        
        # Overwrite the output CSV file with the new data
        output_path = '/Users/jerichlee/Documents/aeren/csv/aggre.csv'
        mean_df.to_csv(output_path, index=False)
        
        self.display_data(mean_data)
    
    def display_data(self, data):
        # Display the data in the Treeview
        for stat, value in zip(data['Stat'], data['Value']):
            self.tree.insert("", tk.END, values=(stat, f"{value:.2f}" if value is not None else ''))

if __name__ == "__main__":
    root = tk.Tk()
    app = DietApp(root)
    root.mainloop()