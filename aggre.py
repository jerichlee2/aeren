import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
from datetime import datetime, timedelta

class DietApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aggregator")

        # Initialize current date to today
        self.current_date = pd.to_datetime(datetime.now().strftime('%Y-%m-%d'))

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

        # Add navigation buttons
        self.back_button = tk.Button(root, text="<", command=self.go_back)
        self.back_button.pack(side=tk.LEFT, padx=10)

        self.forward_button = tk.Button(root, text=">", command=self.go_forward)
        self.forward_button.pack(side=tk.RIGHT, padx=10)

        # Process the CSV files upon initialization
        self.process_csv()

    def process_csv(self):
        diet_data = self.process_diet_csv(self.current_date)
        books_data = self.process_books_csv(self.current_date)
        deepwork_data = self.process_deepwork_csv(self.current_date)
        lifting_data = self.process_lifting_csv(self.current_date)  # Process lifting.csv for Active Zone Minutes

        mean_data = {
            'Stat': [
                'Mean Calories/Day (Last 7 Days)',
                'Mean Carbs (g)/Day (Last 7 Days)',
                'Mean Protein (g)/Day (Last 7 Days)',
                'Mean Fat (g)/Day (Last 7 Days)',
                'Weekly Average Time Reading (Hours)',
                'Weekly Average Deep Work Time (Hours)',
                'Weekly Average Active Zone Minutes',
                f"Calories ({self.current_date.strftime('%Y-%m-%d')})",
                f"Carbs (g) ({self.current_date.strftime('%Y-%m-%d')})",
                f"Protein (g) ({self.current_date.strftime('%Y-%m-%d')})",
                f"Fat (g) ({self.current_date.strftime('%Y-%m-%d')})",
                f"Time Reading (Hours) ({self.current_date.strftime('%Y-%m-%d')})",
                f"Deep Work Time (Hours) ({self.current_date.strftime('%Y-%m-%d')})",
                f"Active Zone Minutes ({self.current_date.strftime('%Y-%m-%d')})"
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

        self.display_data(mean_data)

    def process_diet_csv(self, current_date):
        diet_file_path = '/Users/jerichlee/Documents/aeren/csv/diet.csv'

        if not os.path.exists(diet_file_path):
            messagebox.showerror("Error", "Diet file not found!")
            return

        diet_df = pd.read_csv(diet_file_path)
        diet_df = diet_df[['Calories', 'Carbs (g)', 'Protein (g)', 'Fat (g)', 'Date']]
        diet_df['Date'] = pd.to_datetime(diet_df['Date'], format='%Y-%m-%d')

        last_week = current_date - timedelta(days=6)
        date_range = pd.date_range(last_week, current_date)
        diet_df_last_week = diet_df[diet_df['Date'].isin(date_range)]

        daily_sums_last_week = diet_df_last_week.groupby('Date').sum().reindex(date_range, fill_value=0)
        mean_values_last_week = daily_sums_last_week.mean().round(2).to_dict()

        today_values = daily_sums_last_week.loc[current_date].round(2).to_dict() if current_date in daily_sums_last_week.index else {
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
    
    def process_books_csv(self, current_date):
        books_file_path = '/Users/jerichlee/Documents/aeren/csv/books.csv'

        if not os.path.exists(books_file_path):
            messagebox.showerror("Error", "Books file not found!")
            return [0.0, 0.0]

        books_df = pd.read_csv(books_file_path)
        books_df['Date'] = pd.to_datetime(books_df['Date'], format='%Y-%m-%d')
        books_df['Start Time'] = pd.to_datetime(books_df['Start Time'], format='%I:%M %p', errors='coerce')
        books_df['End Time'] = pd.to_datetime(books_df['End Time'], format='%I:%M %p', errors='coerce')
        books_df['Duration'] = (books_df['End Time'] - books_df['Start Time']).dt.total_seconds() / 3600

        last_week = current_date - timedelta(days=6)
        date_range = pd.date_range(last_week, current_date)
        books_df_last_week = books_df[(books_df['Date'] >= last_week) & (books_df['Date'] <= current_date)]

        daily_reading_time = books_df_last_week.groupby('Date')['Duration'].sum().reindex(date_range, fill_value=0)
        total_reading_time_last_week = daily_reading_time.sum()
        weekly_avg_reading_time = (total_reading_time_last_week / 7).round(3)

        today_reading_time = daily_reading_time.loc[current_date]

        return [weekly_avg_reading_time, today_reading_time]

    def process_deepwork_csv(self, current_date):
        deepwork_file_path = '/Users/jerichlee/Documents/aeren/csv/deepwork.csv'

        if not os.path.exists(deepwork_file_path):
            messagebox.showerror("Error", "Deep Work file not found!")
            return [0.0, 0.0]

        deepwork_df = pd.read_csv(deepwork_file_path)
        deepwork_df['Date'] = pd.to_datetime(deepwork_df['Date'], format='%Y-%m-%d')
        deepwork_df['Start Time'] = pd.to_datetime(deepwork_df['Start Time'], format='%I:%M %p')
        deepwork_df['End Time'] = pd.to_datetime(deepwork_df['End Time'], format='%I:%M %p')
        deepwork_df['Duration'] = (deepwork_df['End Time'] - deepwork_df['Start Time']).dt.total_seconds() / 3600

        last_week = current_date - timedelta(days=6)
        date_range = pd.date_range(last_week, current_date)
        deepwork_df_last_week = deepwork_df[(deepwork_df['Date'] >= last_week) & (deepwork_df['Date'] <= current_date)]

        daily_deepwork_time = deepwork_df_last_week.groupby('Date')['Duration'].sum().reindex(date_range, fill_value=0)
        total_deepwork_time_last_week = daily_deepwork_time.sum()
        weekly_avg_deepwork_time = (total_deepwork_time_last_week / 7).round(3)

        today_deepwork_time = daily_deepwork_time.loc[current_date]

        return [weekly_avg_deepwork_time, today_deepwork_time]

    def process_lifting_csv(self, current_date):
        lifting_file_path = '/Users/jerichlee/Documents/aeren/csv/lifting.csv'

        if not os.path.exists(lifting_file_path):
            messagebox.showerror("Error", "Lifting file not found!")
            return [0.0, 0.0]

        lifting_df = pd.read_csv(lifting_file_path)
        lifting_df['Date'] = pd.to_datetime(lifting_df['Date'], format='%Y-%m-%d')

        lifting_df['Active Zone Minutes'] = pd.to_numeric(lifting_df['Active Zone Minutes'], errors='coerce')

        last_week = current_date - timedelta(days=6)
        date_range = pd.date_range(last_week, current_date)
        lifting_df_last_week = lifting_df[(lifting_df['Date'] >= last_week) & (lifting_df['Date'] <= current_date)]

        daily_active_zone_minutes = lifting_df_last_week.groupby('Date')['Active Zone Minutes'].sum().reindex(date_range, fill_value=0)
        weekly_avg_active_zone_minutes = (daily_active_zone_minutes.sum() / 7).round(2)

        today_active_zone_minutes = daily_active_zone_minutes.loc[current_date]

        return [weekly_avg_active_zone_minutes, today_active_zone_minutes]

    # Similarly update process_books_csv, process_deepwork_csv, process_lifting_csv methods to accept current_date

    def go_back(self):
        self.current_date -= timedelta(days=1)
        self.update_buttons()
        self.process_csv()

    def go_forward(self):
        today_date = pd.to_datetime(datetime.now().strftime('%Y-%m-%d'))
        if self.current_date >= today_date:
            messagebox.showerror("Error", "Cannot go into the future!")
        else:
            self.current_date += timedelta(days=1)
            self.update_buttons()
            self.process_csv()

    def update_buttons(self):
        today_date = pd.to_datetime(datetime.now().strftime('%Y-%m-%d'))
        if self.current_date >= today_date:
            self.forward_button.config(state=tk.DISABLED)
        else:
            self.forward_button.config(state=tk.NORMAL)

    def display_data(self, data):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Display the data in the Treeview
        for stat, value in zip(data['Stat'], data['Value']):
            self.tree.insert("", tk.END, values=(stat, f"{value:.2f}" if value is not None else ''))



if __name__ == "__main__":
    root = tk.Tk()
    app = DietApp(root)
    root.mainloop()