import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
from datetime import datetime, timedelta
import numpy as np

class DietApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Aggregator")

        # Initialize current date to today
        self.current_date = pd.to_datetime(datetime.now().strftime('%Y-%m-%d'))

        # Create a frame for the data display
        self.frame = tk.Frame(root)
        self.frame.pack(pady=20, fill=tk.BOTH, expand=True)

        # Create a Treeview widget with four columns
        self.tree = ttk.Treeview(self.frame, columns=("Weekly Mean Stat", "Weekly Mean Value", "Today's Value", "Goals"), show='headings')
        self.tree.heading("Weekly Mean Stat", text="Stat")
        self.tree.heading("Weekly Mean Value", text="Weekly Mean Value")
        self.tree.heading("Today's Value", text="Today's Value")
        self.tree.heading("Goals", text="Goals")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a vertical scrollbar
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Add a label to display the current date with smaller padding
        self.date_label = tk.Label(root, text=self.current_date.strftime('%a %b %d, %Y'))
        self.date_label.pack(pady=5)  # Reduced padding to 5

        # Add navigation buttons
        self.back_button = tk.Button(root, text="<", command=self.go_back)
        self.back_button.pack(side=tk.LEFT, padx=10)

        self.forward_button = tk.Button(root, text=">", command=self.go_forward)
        self.forward_button.pack(side=tk.RIGHT, padx=10)

        # Add reset button to go back to the current day
        self.reset_button = tk.Button(root, text="Reset", command=self.reset_to_today)
        self.reset_button.pack(side=tk.BOTTOM, pady=10)

        # Process the CSV files upon initialization
        self.process_csv()

    def process_csv(self):
        diet_data = self.process_diet_csv(self.current_date)
        books_data = self.process_books_csv(self.current_date)
        deepwork_data = self.process_deepwork_csv(self.current_date)
        lifting_data = self.process_lifting_csv(self.current_date)  # Process lifting.csv for Active Zone Minutes
        calm_data = self.process_calm_csv(self.current_date)
        goals_values = self.process_goals_csv()

        # Create lists for weekly mean and today's data
        weekly_mean_stats = [
            'Cals 🥙',
            'Carbs 🍞',
            'Protein 🥩',
            'Fat 🧈',
            'Reading 📖',
            'Deepwork 📝',
            'Active 🏋️',
            'Meditate 🧘'
        ]

        weekly_mean_values = diet_data['mean_values'] + books_data[:1] + deepwork_data[:1] + lifting_data[:1] + calm_data[:1]
        todays_values = diet_data['today_values'] + books_data[1:] + deepwork_data[1:] + lifting_data[1:] + calm_data[1:]

        # Calculate MSE_max using historical data
        mse_max = self.calculate_constant_mse_max(self.category_bounds)

        # Calculate scores based on today's values, goals, and MSE_max
        scores = [self.calculate_score(today, goal, mse_max) for today, goal in zip(todays_values, goals_values)]

        # Create a list of tuples to pair stats, values, and scores
        data = list(zip(weekly_mean_stats, weekly_mean_values, todays_values, goals_values, scores))

        self.display_data(data)

    def calculate_constant_mse_max(self,category_bounds):
        total_mse_max = 0

        for category, bounds in category_bounds.items():
            min_value, max_value = bounds
            # Calculate the maximum difference
            max_diff = max_value - min_value
            
            # Use the middle of the range as the expected value
            expected_value = (min_value + max_value) / 2
            
            # Normalize the difference by the expected value to get the relative error
            normalized_diff = max_diff / expected_value if expected_value != 0 else 0
            
            # Square the normalized difference
            squared_diff = normalized_diff ** 2
            
            # Add to total MSE_max
            total_mse_max += squared_diff
        
        return total_mse_max

    def calculate_score(self, today_value, goal_value, mse_max):
        # Calculate the MSE for today's values
        difference = today_value - goal_value
        normalized_diff = difference / (goal_value if goal_value != 0 else 1)
        mse = normalized_diff ** 2

        # Calculate the score using MSE and MSE_max
        score = 100 * (1 - (mse / mse_max))
        return max(0, min(100, score))

    # Rest of your class implementation, including other CSV processing methods...

    def display_data(self, data):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Display the data in the Treeview
        for mean_stat, mean_value, today_value, goals_values, score in data:
            self.tree.insert("", tk.END, values=(
                mean_stat,
                f"{mean_value:.2f}" if mean_value is not None else '',
                f"{today_value:.2f}" if today_value is not None else '',
                goals_values))

    # Other methods like process_diet_csv, go_back, go_forward, etc...

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
    
    def process_calm_csv(self, current_date):
        calm_file_path = '/Users/jerichlee/Documents/aeren/csv/calm.csv'

        if not os.path.exists(calm_file_path):
            messagebox.showerror("Error", "Books file not found!")
            return [0.0, 0.0]

        calm_df = pd.read_csv(calm_file_path)
        calm_df['Date'] = pd.to_datetime(calm_df['Date'], format='%Y-%m-%d')
        calm_df['Start Time'] = pd.to_datetime(calm_df['Start Time'], format='%I:%M %p', errors='coerce')
        calm_df['End Time'] = pd.to_datetime(calm_df['End Time'], format='%I:%M %p', errors='coerce')
        calm_df['Duration'] = (calm_df['End Time'] - calm_df['Start Time']).dt.total_seconds() / 3600

        last_week = current_date - timedelta(days=6)
        date_range = pd.date_range(last_week, current_date)
        calm_df_last_week = calm_df[(calm_df['Date'] >= last_week) & (calm_df['Date'] <= current_date)]

        daily_calm_time = calm_df_last_week.groupby('Date')['Duration'].sum().reindex(date_range, fill_value=0)
        total_calm_time_last_week = daily_calm_time.sum()
        weekly_avg_calm_time = (total_calm_time_last_week / 7).round(3)

        today_calm_time = daily_calm_time.loc[current_date]

        return [weekly_avg_calm_time, today_calm_time]
    
    def process_goals_csv(self):
        goals_file_path = '/Users/jerichlee/Documents/aeren/csv/goals.csv'
        if not os.path.exists(goals_file_path):
            messagebox.showerror("Error", "Goals file not found!")
            return ["N/A"] * 7  # Return default values if file is not found

        goals_df = pd.read_csv(goals_file_path)
        goals_df['Date'] = pd.to_datetime(goals_df['Date'], format='%m/%d/%y')
        latest_goals = goals_df.sort_values(by='Date', ascending=False).iloc[0]

        # Extract goal values in the order corresponding to your stats
        goals_values = [
            latest_goals['Calories 🥙'],
            latest_goals['Carbs 🍞'],
            latest_goals['Protein 🥩'],
            latest_goals['Fat 🧈'],
            latest_goals['Time Reading 📖'],
            latest_goals['Deepwork Time 📝'],
            latest_goals['Active Time 🏋️'],
            latest_goals['Meditation 🧘']
        ]
        return goals_values

    def go_back(self):
        self.current_date -= timedelta(days=1)
        self.update_date_label()
        self.update_buttons()
        self.process_csv()

    def go_forward(self):
        today_date = pd.to_datetime(datetime.now().strftime('%Y-%m-%d'))
        if self.current_date >= today_date:
            messagebox.showerror("Error", "Cannot go into the future!")
        else:
            self.current_date += timedelta(days=1)
            self.update_date_label()
            self.update_buttons()
            self.process_csv()

    def reset_to_today(self):
        self.current_date = pd.to_datetime(datetime.now().strftime('%Y-%m-%d'))
        self.update_date_label()
        self.update_buttons()
        self.process_csv()

    def update_date_label(self):
        # Update the date label with the current date in the desired format
        self.date_label.config(text=self.current_date.strftime('%a %b %d, %Y'))

    def update_buttons(self):
        today_date = pd.to_datetime(datetime.now().strftime('%Y-%m-%d'))
        if self.current_date >= today_date:
            self.forward_button.config(state=tk.DISABLED)
        else:
            self.forward_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = DietApp(root)
    root.mainloop()


