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

        # Create a Treeview widget with four columns (removed 'Score' column)
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
        lifting_data = self.process_lifting_csv(self.current_date)
        calm_data = self.process_calm_csv(self.current_date)
        goals_values = self.process_goals_csv()
        
        # Calculate MSE_max using category ranges
        mse_max = self.calculate_constant_mse_max(goals_values)

        # Update weekly_mean_stats to include "Score ✅"
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

        # Combine data for weekly means and today's values
        weekly_mean_values = diet_data['mean_values'] + books_data[:1] + deepwork_data[:1] + lifting_data[:1] + calm_data[:1]
        todays_values = diet_data['today_values'] + books_data[1:] + deepwork_data[1:] + lifting_data[1:] + calm_data[1:]

        # Round goals_values based on the stat type
        rounded_goals_values = self.round_goals_values(goals_values)

# Calculate scores based on today's values, goals, and MSE_max
        today_score = self.calculate_score(todays_values, goals_values, mse_max, cap_score=True)
        weekly_mean_score = self.calculate_score(weekly_mean_values, goals_values, mse_max, cap_score=False)

        # Calculate the letter grades for the scores
        today_letter_grade = self.get_letter_grade(today_score)
        weekly_mean_letter_grade = self.get_letter_grade(weekly_mean_score)

        # Create the data list
        data = []
        for mean_stat, mean_value, today_value, goal_value in zip(weekly_mean_stats, weekly_mean_values, todays_values, rounded_goals_values):
            data.append((mean_stat, mean_value, today_value, goal_value))

        # Add the overall scores row with letter grades
        today_score_with_grade = f"{today_score:.2f} ({today_letter_grade})"
        weekly_mean_score_with_grade = f"{weekly_mean_score:.2f} ({weekly_mean_letter_grade})"
        data.append(('Score ✅', weekly_mean_score_with_grade, today_score_with_grade, ''))

        # Display data in the Treeview
        self.display_data(data)

        # Append today's score to CSV without the letter grade
        self.append_scores_to_csv(today_score)
        # print(mse_max)

    def round_goals_values(self, goals_values):
        # Rounding logic based on the type of stat
        rounded_values = []
        for stat, value in zip([
            'Cals 🥙', 'Carbs 🍞', 'Protein 🥩', 'Fat 🧈',
            'Reading 📖', 'Deepwork 📝', 'Active 🏋️', 'Meditate 🧘'], goals_values):
            if stat in ['Cals 🥙', 'Carbs 🍞', 'Protein 🥩', 'Fat 🧈', 'Active 🏋️', 'Meditate 🧘']:
                rounded_values.append(round(value))  # Round to nearest integer
            elif stat in ['Reading 📖', 'Deepwork 📝']:
                rounded_values.append(round(value, 1))  # Round to nearest tenth
            else:
                rounded_values.append(value)  # Default case, should not happen
        return rounded_values

    def get_letter_grade(self, score):
        if 93 <= score <= 100:
            return 'A'
        elif 90 <= score < 93:
            return 'A-'
        elif 87 <= score < 90:
            return 'B+'
        elif 83 <= score < 87:
            return 'B'
        elif 80 <= score < 83:
            return 'B-'
        elif 77 <= score < 80:
            return 'C+'
        elif 73 <= score < 77:
            return 'C'
        elif 70 <= score < 73:
            return 'C-'
        elif 67 <= score < 70:
            return 'D+'
        elif 63 <= score < 67:
            return 'D'
        elif 60 <= score < 63:
            return 'D-'
        else:
            return 'F'

    def display_data(self, data):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Display the data in the Treeview
        for mean_stat, mean_value, today_value, goals_values in data:
            self.tree.insert("", tk.END, values=(
                mean_stat,
                str(mean_value) if mean_value is not None else '',
                str(today_value) if today_value is not None else '',
                str(goals_values) if goals_values is not None else ''
            ))

    def append_scores_to_csv(self, score):
        scores_file_path = '/Users/jerichlee/Documents/aeren/csv/scores.csv'
        current_date_str = self.current_date.strftime('%Y-%m-%d')
        
        # Create a DataFrame for the new score
        new_scores_df = pd.DataFrame({'score': [score], 'date': [current_date_str]})
        
        # Check if the scores file exists
        if os.path.exists(scores_file_path):
            # Read the existing scores
            existing_scores_df = pd.read_csv(scores_file_path)
            
            # Check if the current date is already in the file
            if current_date_str in existing_scores_df['date'].values:
                # Replace the row with the same date
                existing_scores_df.loc[existing_scores_df['date'] == current_date_str, 'score'] = score
            else:
                # Append the new score
                existing_scores_df = pd.concat([existing_scores_df, new_scores_df], ignore_index=True)
        else:
            # If the file doesn't exist, just use the new DataFrame
            existing_scores_df = new_scores_df
        
        # Sort the DataFrame by date in ascending order
        existing_scores_df['date'] = pd.to_datetime(existing_scores_df['date'])
        sorted_scores_df = existing_scores_df.sort_values(by='date', ascending=True)
        
        # Save the sorted DataFrame back to the CSV
        sorted_scores_df.to_csv(scores_file_path, index=False)

    def append_scores_to_csv(self, score):
        scores_file_path = '/Users/jerichlee/Documents/aeren/csv/scores.csv'
        current_date_str = self.current_date.strftime('%Y-%m-%d')
        
        # Create a DataFrame for the new score
        new_scores_df = pd.DataFrame({'score': [score], 'date': [current_date_str]})
        
        # Check if the scores file exists
        if os.path.exists(scores_file_path):
            # Read the existing scores
            existing_scores_df = pd.read_csv(scores_file_path)
            
            # Check if the current date is already in the file
            if current_date_str in existing_scores_df['date'].values:
                # Replace the row with the same date
                existing_scores_df.loc[existing_scores_df['date'] == current_date_str, 'score'] = score
            else:
                # Append the new score
                existing_scores_df = pd.concat([existing_scores_df, new_scores_df], ignore_index=True)
        else:
            # If the file doesn't exist, just use the new DataFrame
            existing_scores_df = new_scores_df
        
        # Sort the DataFrame by date in ascending order
        existing_scores_df['date'] = pd.to_datetime(existing_scores_df['date'])
        sorted_scores_df = existing_scores_df.sort_values(by='date', ascending=True)
        
        # Save the sorted DataFrame back to the CSV
        sorted_scores_df.to_csv(scores_file_path, index=False)

    def process_goals_csv(self):
        goals_file_path = '/Users/jerichlee/Documents/aeren/csv/goals.csv'
        
        if not os.path.exists(goals_file_path):
            messagebox.showerror("Error", "Goals file not found!")
            return ["N/A"] * 8, {}  # Return default values if file is not found

        # Read the goals.csv file
        goals_df = pd.read_csv(goals_file_path, header=None)

        # Identify rows with dates and parse them
        date_rows = pd.to_datetime(goals_df.iloc[:, 0], errors='coerce').dropna().index
        
        # Find the most recent date that is less than or equal to the current date
        latest_date_index = None
        for index in date_rows:
            date = pd.to_datetime(goals_df.iloc[index, 0])
            if date <= self.current_date:
                latest_date_index = index

        if latest_date_index is None:
            messagebox.showerror("Error", "No valid goals found for the current date!")
            return ["N/A"] * 8, {}

        # Extract the latest date's goals and range
        goal_values = goals_df.iloc[latest_date_index + 1, 1:].astype(float).tolist()

        # # Extract range values, remove quotes and convert to tuples
        # range_strings = goals_df.iloc[latest_date_index + 2, 1:].tolist()
        # range_values = []
        # for range_str in range_strings:
        #     min_val, max_val = map(int, range_str.strip('"()').split(','))
        #     range_values.append((min_val, max_val))

        return goal_values

    def calculate_score(self, values, goals_values, mse_max, cap_score=False):
        # Adjust values if they exceed goals
        adjusted_values = [
            min(value, goal) for value, goal in zip(values, goals_values)
        ]

        # Calculate MSE
        mse = 0
        for value, goal_value in zip(adjusted_values, goals_values):
            difference = value - goal_value
            normalized_diff = difference / (goal_value if goal_value != 0 else 1)
            mse += normalized_diff ** 2

        mse /= len(values)

        # Calculate the score using MSE and MSE_max
        score = 100 * (1 - (mse / mse_max))

        # Apply the cap if required
        if cap_score:
            if any(value == 0 and goal != 0 for value, goal in zip(values, goals_values)):
                score = min(score, 89)  # Cap score at B+ if there's a zero value and the goal is not zero
            elif any(value < 0.9 * goal for value, goal in zip(adjusted_values, goals_values)):
                score = min(score, 90)  # Cap score at A- if not within 10% of goal
        return max(0, min(100, score))

    def calculate_constant_mse_max(self, goals_values):
        # Calculate the constant MSE_max using 30% of each goal value
        total_mse_max = 0

        for goal_value in goals_values:
            max_range = goal_value * 1.3  # 30% above the goal
            difference = max_range - goal_value
            normalized_diff = difference / (goal_value if goal_value != 0 else 1)
            squared_diff = normalized_diff ** 2
            total_mse_max += squared_diff

        return total_mse_max


    def append_scores_to_csv(self, scores):
        scores_file_path = '/Users/jerichlee/Documents/aeren/csv/scores.csv'
        current_date_str = self.current_date.strftime('%Y-%m-%d')
        
        # Calculate the overall average score for the day
        average_score = np.mean(scores)
        
        # Create a DataFrame for the new score
        new_scores_df = pd.DataFrame({'score': [average_score], 'date': [current_date_str]})
        
        # Check if the scores file exists
        if os.path.exists(scores_file_path):
            # Read the existing scores
            existing_scores_df = pd.read_csv(scores_file_path)
            
            # Check if the current date is already in the file
            if current_date_str in existing_scores_df['date'].values:
                # Replace the row with the same date
                existing_scores_df.loc[existing_scores_df['date'] == current_date_str, 'score'] = average_score
            else:
                # Append the new score
                existing_scores_df = pd.concat([existing_scores_df, new_scores_df], ignore_index=True)
        else:
            # If the file doesn't exist, just use the new DataFrame
            existing_scores_df = new_scores_df
        
        # Sort the DataFrame by date in descending order
        existing_scores_df['date'] = pd.to_datetime(existing_scores_df['date'])
        sorted_scores_df = existing_scores_df.sort_values(by='date', ascending=True)
        
        # Save the sorted DataFrame back to the CSV
        sorted_scores_df.to_csv(scores_file_path, index=False)

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
                round(mean_values_last_week.get('Calories', 0.0)),
                               round(mean_values_last_week.get('Carbs (g)', 0.0)),
                round(mean_values_last_week.get('Protein (g)', 0.0)),
                round(mean_values_last_week.get('Fat (g)', 0.0))
            ],
            'today_values': [
                round(today_values.get('Calories', 0.0)),
                round(today_values.get('Carbs (g)', 0.0)),
                round(today_values.get('Protein (g)', 0.0)),
                round(today_values.get('Fat (g)', 0.0))
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
        books_df.loc[books_df['Duration'] < 0, 'Duration'] += 24  # Adjust for overnight time spans

        last_week = current_date - timedelta(days=6)
        date_range = pd.date_range(last_week, current_date)
        books_df_last_week = books_df[(books_df['Date'] >= last_week) & (books_df['Date'] <= current_date)]

        daily_reading_time = books_df_last_week.groupby('Date')['Duration'].sum().reindex(date_range, fill_value=0)
        total_reading_time_last_week = daily_reading_time.sum()
        weekly_avg_reading_time = (total_reading_time_last_week / 7).round(3)

        today_reading_time = daily_reading_time.loc[current_date] if current_date in daily_reading_time else 0.0

        return [weekly_avg_reading_time.round(1), today_reading_time.round(1)]

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
        deepwork_df.loc[deepwork_df['Duration'] < 0, 'Duration'] += 24  # Adjust for overnight time spans
        deepwork_df['Duration'] = np.floor(deepwork_df['Duration'] * 1000) / 1000

        last_week = current_date - timedelta(days=6)
        date_range = pd.date_range(last_week, current_date)
        deepwork_df_last_week = deepwork_df[(deepwork_df['Date'] >= last_week) & (deepwork_df['Date'] <= current_date)]

        daily_deepwork_time = deepwork_df_last_week.groupby('Date')['Duration'].sum().reindex(date_range, fill_value=0)
        total_deepwork_time_last_week = daily_deepwork_time.sum()
        weekly_avg_deepwork_time = (total_deepwork_time_last_week / 7).round(3)

        today_deepwork_time = daily_deepwork_time.loc[current_date] if current_date in daily_deepwork_time else 0.0

        return [weekly_avg_deepwork_time.round(1), today_deepwork_time.round(1)]

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

        today_active_zone_minutes = daily_active_zone_minutes.loc[current_date] if current_date in daily_active_zone_minutes else 0.0

        return [round(weekly_avg_active_zone_minutes), round(today_active_zone_minutes)]
    
    def process_calm_csv(self, current_date):
        calm_file_path = '/Users/jerichlee/Documents/aeren/csv/calm.csv'

        if not os.path.exists(calm_file_path):
            messagebox.showerror("Error", "Calm file not found!")
            return [0.0, 0.0]

        calm_df = pd.read_csv(calm_file_path)
        calm_df['Date'] = pd.to_datetime(calm_df['Date'], format='%Y-%m-%d')
        calm_df['Start Time'] = pd.to_datetime(calm_df['Start Time'], format='%I:%M %p', errors='coerce')
        calm_df['End Time'] = pd.to_datetime(calm_df['End Time'], format='%I:%M %p', errors='coerce')
        calm_df['Duration'] = (calm_df['End Time'] - calm_df['Start Time']).dt.total_seconds() / 60
        calm_df.loc[calm_df['Duration'] < 0, 'Duration'] += 24*60  # Adjust for overnight time spans

        last_week = current_date - timedelta(days=6)
        date_range = pd.date_range(last_week, current_date)
        calm_df_last_week = calm_df[(calm_df['Date'] >= last_week) & (calm_df['Date'] <= current_date)]

        daily_calm_time = calm_df_last_week.groupby('Date')['Duration'].sum().reindex(date_range, fill_value=0)
        total_calm_time_last_week = daily_calm_time.sum()
        weekly_avg_calm_time = (total_calm_time_last_week / 7).round(3)

        today_calm_time = daily_calm_time.loc[current_date] if current_date in daily_calm_time else 0.0

        return [round(weekly_avg_calm_time), round(today_calm_time)]

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