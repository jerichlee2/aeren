import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os
from datetime import datetime

class DietApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Diet Data Processor")
        
        # Create a frame for the data display
        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)
        
        # Process the CSV file upon initialization
        self.process_csv()

    def process_csv(self):
        file_path = '/Users/jerichlee/Documents/aeren/csv/diet.csv'
        
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "File not found!")
            return
        
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Focus on the specified columns
        df = df[['Calories', 'Carbs (g)', 'Protein (g)', 'Fat (g)', 'Date']]
        
        # Convert Date column to datetime with specified format
        df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y')
        
        # Group by Date and calculate daily sums
        daily_sums = df.groupby('Date').sum()
        
        # Compute the mean of each day and convert to integer
        mean_values = daily_sums.mean().round().astype(int).to_dict()
        
        # Get today's date
        today_date = pd.to_datetime(datetime.now().strftime('%m/%d/%y'))
        
        # Filter today's values and convert to integer
        if today_date in daily_sums.index:
            today_values = daily_sums.loc[today_date].round().astype(int).to_dict()
        else:
            today_values = {
                'Calories': 0,
                'Carbs (g)': 0,
                'Protein (g)': 0,
                'Fat (g)': 0
            }
        
        # Prepare the data to append
        mean_data = {
            'Stat': [
                'Mean Calories/Day',
                'Mean Carbs (g)/Day',
                'Mean Protein (g)/Day',
                'Mean Fat (g)/Day',
                'Mean Time Read/Day',
                'Mean Deepwork/Day',
                'Mean FBZ/Day',
                "Today's Calories",
                "Today's Carbs (g)",
                "Today's Protein (g)",
                "Today's Fat (g)",
                "Today's Time Read",
                "Today's Deepwork",
                "Today's FBZ"
            ],
            'Value': [
                mean_values.get('Calories', 0),
                mean_values.get('Carbs (g)', 0),
                mean_values.get('Protein (g)', 0),
                mean_values.get('Fat (g)', 0),
                None,
                None,
                None,
                today_values.get('Calories', 0),
                today_values.get('Carbs (g)', 0),
                today_values.get('Protein (g)', 0),
                today_values.get('Fat (g)', 0),
                None,
                None,
                None
            ]
        }
        
        mean_df = pd.DataFrame(mean_data)
        
        # Append the mean values to the output CSV file
        output_path = '/Users/jerichlee/Documents/aeren/csv/aggre.csv'
        if os.path.exists(output_path):
            mean_df.to_csv(output_path, mode='a', header=False, index=False)
        else:
            mean_df.to_csv(output_path, index=False)
        
        self.display_data(mean_data)
    
    def display_data(self, data):
        # Display the data in the GUI
        for idx, (stat, value) in enumerate(zip(data['Stat'], data['Value'])):
            tk.Label(self.frame, text=stat).grid(row=idx, column=0, padx=10, pady=5)
            tk.Label(self.frame, text=int(value) if value is not None else '').grid(row=idx, column=1, padx=10, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = DietApp(root)
    root.mainloop()