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
        diet_data = self.process_diet_csv()
        books_data = self.process_books_csv()
        deepwork_data = self.process_deepwork_csv()
        lifting_data = self.process_lifting_csv()  # Process lifting.csv for Active Zone Minutes
        
        # Reordering the data: Weekly data first, then daily data
        mean_data = {
            'Stat': [
                'Mean Calories/Day (Last 7 Days)',
                'Mean Carbs (g)/Day (Last 7 Days)',
                'Mean Protein (g)/Day (Last 7 Days)',
                'Mean Fat (g)/Day (Last 7 Days)',
                'Weekly Average Time Reading (Hours)',
                'Weekly Average Deep Work Time (Hours)',
                'Weekly Average Active Zone Minutes',
                "Today's Calories",
                "Today's Carbs (g)",
                "Today's Protein (g)",
                "Today's Fat (g)",
                "Today's Time Reading (Hours)",
                "Today's Deep Work Time (Hours)",
                "Today's Active Zone Minutes"
            ],
            'Value': (
                diet_data['mean_values'] +
                books_data[:1] +
                deepwork_data[:1] +
                lifting_data[:1] +
                diet_data['today_values'] +
                books_data[1:] +
                deepwork_data[1:] +
                lifting_data[1:]
            )
        }
        
        mean_df = pd.DataFrame(mean_data)
        
        # Overwrite the output CSV file with the new data
        output_path = '/Users/jerichlee/Documents/aeren/csv/aggre.csv'
        mean_df.to_csv(output_path, index=False)
        
        self.display_data(mean_data)
    
    def process_diet_csv(self):
        diet_file_path = '/Users/jerichlee/Documents/aeren/csv/diet.csv'
        
        if not os.path.exists(diet_file_path):
            messagebox.showerror("Error", "Diet file not found!")
            return
        
        diet_df = pd.read_csv(diet_file_path)
        diet_df = diet_df[['Calories', 'Carbs (g)', 'Protein (g)', 'Fat (g)', 'Date']]
        diet_df['Date'] = pd.to_datetime(diet_df['Date'], format='%m/%d/%y')
        
        today_date = pd.to_datetime(datetime.now().strftime('%m/%d/%y'))
        last_week = today_date - timedelta(days=6)
        date_range = pd.date_range(last_week, today_date)
        diet_df_last_week = diet_df[diet_df['Date'].isin(date_range)]
        
        daily_sums_last_week = diet_df_last_week.groupby('Date').sum().reindex(date_range, fill_value=0)
        mean_values_last_week = daily_sums_last_week.mean().round(2).to_dict()
        
        today_values = daily_sums_last_week.loc[today_date].round(2).to_dict() if today_date in daily_sums_last_week.index else {
            'Calories': 0.0,
            'Carbs (g)': 0.0,
            'Protein (g)': 0.0,
            'Fat (g)': 0.0
        }
        
        return {
            'mean_values': [
                mean_values_last_week.get('Calories', 0.0),
                mean_values_last_week.get('Carbs (g)', 0.0),
                mean_values_last_week.get('Protein (g)', 0.0),
                mean_values_last_week.get('Fat (g)', 0.0)
            ],
            'today_values': [
                today_values.get('Calories', 0.0),
                today_values.get('Carbs (g)', 0.0),
                today_values.get('Protein (g)', 0.0),
                today_values.get('Fat (g)', 0.0)
            ]
        }
    
    def process_books_csv(self):
        books_file_path = '/Users/jerichlee/Documents/aeren/csv/books.csv'
        
        if not os.path.exists(books_file_path):
            messagebox.showerror("Error", "Books file not found!")
            return
        
        books_df = pd.read_csv(books_file_path)
        books_df['Date'] = pd.to_datetime(books_df['Date'], format='%Y-%m-%d')
        books_df['Start Time'] = pd.to_datetime(books_df['Start Time'], format='%I:%M %p', errors='coerce')
        books_df['End Time'] = pd.to_datetime(books_df['End Time'], format='%I:%M %p', errors='coerce')
        books_df['Duration'] = (books_df['End Time'] - books_df['Start Time']).dt.total_seconds() / 3600
        
        today_date = pd.to_datetime(datetime.now().strftime('%Y-%m-%d'))
        last_week = today_date - timedelta(days=6)
        date_range = pd.date_range(last_week, today_date)
        books_df_last_week = books_df[(books_df['Date'] >= last_week) & (books_df['Date'] <= today_date)]
        
        daily_reading_time = books_df_last_week.groupby('Date')['Duration'].sum().reindex(date_range, fill_value=0)
        total_reading_time_last_week = daily_reading_time.sum()
        weekly_avg_reading_time = (total_reading_time_last_week / 7).round(3)
        
        today_reading_time = daily_reading_time.loc[today_date]
        
        return [weekly_avg_reading_time, today_reading_time]

    def process_deepwork_csv(self):
        deepwork_file_path = '/Users/jerichlee/Documents/aeren/csv/deepwork.csv'
        
        if not os.path.exists(deepwork_file_path):
            messagebox.showerror("Error", "Deep Work file not found!")
            return
        
        deepwork_df = pd.read_csv(deepwork_file_path)
        deepwork_df['Date'] = pd.to_datetime(deepwork_df['Date'], format='%m/%d/%y')
        deepwork_df['Start Time'] = pd.to_datetime(deepwork_df['Start Time'], format='%I:%M %p')
        deepwork_df['End Time'] = pd.to_datetime(deepwork_df['End Time'], format='%I:%M %p')
        deepwork_df['Duration'] = (deepwork_df['End Time'] - deepwork_df['Start Time']).dt.total_seconds() / 3600
        
        today_date = pd.to_datetime(datetime.now().strftime('%m/%d/%y'))
        last_week = today_date - timedelta(days=6)
        date_range = pd.date_range(last_week, today_date)
        deepwork_df_last_week = deepwork_df[(deepwork_df['Date'] >= last_week) & (deepwork_df['Date'] <= today_date)]
        
        daily_deepwork_time = deepwork_df_last_week.groupby('Date')['Duration'].sum().reindex(date_range, fill_value=0)
        total_deepwork_time_last_week = daily_deepwork_time.sum()
        weekly_avg_deepwork_time = (total_deepwork_time_last_week / 7).round(3)
        
        today_deepwork_time = daily_deepwork_time.loc[today_date]
        
        return [weekly_avg_deepwork_time, today_deepwork_time]
    
    def process_lifting_csv(self):
        lifting_file_path = '/Users/jerichlee/Documents/aeren/csv/lifting.csv'
        
        if not os.path.exists(lifting_file_path):
            messagebox.showerror("Error", "Lifting file not found!")
            return [0.0, 0.0]
        
        lifting_df = pd.read_csv(lifting_file_path)
        lifting_df['Date'] = pd.to_datetime(lifting_df['Date'], format='%m/%d/%y')
        
        lifting_df['Active Zone Minutes'] = pd.to_numeric(lifting_df['Active Zone Minutes'], errors='coerce')
        
        today_date = pd.to_datetime(datetime.now().strftime('%m/%d/%y'))
        last_week = today_date - timedelta(days=6)
        date_range = pd.date_range(last_week, today_date)
        lifting_df_last_week = lifting_df[(lifting_df['Date'] >= last_week) & (lifting_df['Date'] <= today_date)]

        daily_active_zone_minutes = lifting_df_last_week.groupby('Date')['Active Zone Minutes'].sum().reindex(date_range, fill_value=0)
        weekly_avg_active_zone_minutes = (daily_active_zone_minutes.sum() / 7).round(2)
        
        today_active_zone_minutes = daily_active_zone_minutes.loc[today_date]
        
        return [weekly_avg_active_zone_minutes, today_active_zone_minutes]

    def display_data(self, data):
        # Display the data in the Treeview
        for stat, value in zip(data['Stat'], data['Value']):
            self.tree.insert("", tk.END, values=(stat, f"{value:.2f}" if value is not None else ''))

if __name__ == "__main__":
    root = tk.Tk()
    app = DietApp(root)
    root.mainloop() 