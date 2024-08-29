import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Specify the path to the CSV file
file_path = '/Users/jerichlee/Documents/aeren/csv/diet.csv'

def load_and_plot(file_path):
    # Load the CSV file into a pandas dataframe
    diet_data = pd.read_csv(file_path)

    # Normalize the capitalization in the 'Meal' column
    diet_data['Meal'] = diet_data['Meal'].str.lower()

    # Convert the 'Date' column to datetime
    diet_data['Date'] = pd.to_datetime(diet_data['Date'], format='%Y-%m-%d')

    # Calculate daily caloric intake
    daily_calories = diet_data.groupby('Date')['Calories'].sum()

    # Calculate daily macronutrient intake
    daily_macros = diet_data.groupby('Date')[['Carbs (g)', 'Protein (g)', 'Fat (g)']].sum()

    # Calculate meal type contributions to daily caloric intake
    meal_contributions = diet_data.groupby(['Date', 'Meal'])['Calories'].sum().unstack()

    # Plotting
    fig, axes = plt.subplots(2, 1, figsize=(10, 5))

    # Daily Caloric Intake
    axes[0].plot(daily_calories, marker='o', linestyle='-', color='b', markersize=2, linewidth=0.5)
    axes[0].set_title('Daily Caloric Intake', fontsize=3)
    axes[0].set_xlabel('')
    axes[0].set_ylabel('Calories', fontsize=3)
    axes[0].tick_params(axis='both', which='major', labelsize=3)
    axes[0].set_xticks([])
    axes[0].grid(True)  # General grid enable

    # Macronutrient Distribution
    daily_macros.plot(kind='bar', stacked=True, ax=axes[1], colormap='viridis')
    axes[1].set_title('Daily Macronutrient Distribution', fontsize=3)
    axes[1].set_xlabel('')
    axes[1].set_ylabel('Grams', fontsize=3)
    axes[1].legend(['Carbs (g)', 'Protein (g)', 'Fat (g)'], loc='best', fontsize=3)
    axes[1].tick_params(axis='both', which='major', labelsize=3)
    axes[1].set_xticks([])
    # axes[1].grid(True)  # General grid enable

    # # Meal Contributions to Daily Caloric Intake
    # meal_contributions.plot(kind='bar', stacked=True, ax=axes[2], colormap='tab20')
    # axes[2].set_title('Meal Contributions to Daily Caloric Intake', fontsize=3)
    # axes[2].set_xlabel('Date', fontsize=3)
    # axes[2].set_ylabel('Calories', fontsize=3)
    # axes[2].legend(loc='best', fontsize=3)
    # axes[2].tick_params(axis='both', which='major', labelsize=4)
    # axes[2].tick_params(axis='x', rotation=90)
    # axes[2].set_xticklabels([date.strftime('%m/%d') for date in meal_contributions.index], fontsize=3)
    # # axes[2].grid(True)  # General grid enable

    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2, hspace=0.5)

    # Display plot in tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Create the main window
root = tk.Tk()
root.title("Food")

# Load and plot the data from the specified file path
load_and_plot(file_path)

# Run the application
root.mainloop()