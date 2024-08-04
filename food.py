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
    diet_data['Date'] = pd.to_datetime(diet_data['Date'], format='%m/%d/%y')

    # Calculate daily caloric intake
    daily_calories = diet_data.groupby('Date')['Calories'].sum()

    # Calculate daily macronutrient intake
    daily_macros = diet_data.groupby('Date')[['Carbs (g)', 'Protein (g)', 'Fat (g)']].sum()

    # Calculate meal type contributions to daily caloric intake
    meal_contributions = diet_data.groupby(['Date', 'Meal'])['Calories'].sum().unstack()

    # Calculate weekly statistics
    mean_calories = daily_calories.mean()
    mean_carbs = daily_macros['Carbs (g)'].mean()
    mean_protein = daily_macros['Protein (g)'].mean()
    mean_fat = daily_macros['Fat (g)'].mean()

    # Plotting
    fig, axes = plt.subplots(4, 1, figsize=(10, 10))

    # Daily Caloric Intake
    axes[0].plot(daily_calories, marker='o', linestyle='-', color='b')
    axes[0].set_title('Daily Caloric Intake', fontsize=10)
    axes[0].set_xlabel('')
    axes[0].set_ylabel('Calories', fontsize=8)
    axes[0].tick_params(axis='both', which='major', labelsize=8)
    axes[0].set_xticks([])

    # Macronutrient Distribution
    daily_macros.plot(kind='bar', stacked=True, ax=axes[1], colormap='viridis')
    axes[1].set_title('Daily Macronutrient Distribution', fontsize=10)
    axes[1].set_xlabel('')
    axes[1].set_ylabel('Grams', fontsize=8)
    axes[1].legend(['Carbs (g)', 'Protein (g)', 'Fat (g)'], fontsize=8)
    axes[1].tick_params(axis='both', which='major', labelsize=8)
    axes[1].set_xticks([])

    # Meal Contributions to Daily Caloric Intake
    meal_contributions.plot(kind='bar', stacked=True, ax=axes[2], colormap='tab20')
    axes[2].set_title('Meal Contributions to Daily Caloric Intake', fontsize=10)
    axes[2].set_xlabel('Date', fontsize=8)
    axes[2].set_ylabel('Calories', fontsize=8)
    axes[2].legend(title='Meal', fontsize=8)
    axes[2].tick_params(axis='both', which='major', labelsize=8)
    axes[2].tick_params(axis='x', rotation=90)
    axes[2].set_xticklabels([date.strftime('%m/%d/%y') for date in meal_contributions.index], fontsize=6)

    # Display weekly statistics
    stats_text = f"Mean Calories/Day: {mean_calories:.2f}\n" \
                 f"Mean Carbs (g)/Day: {mean_carbs:.2f}\n" \
                 f"Mean Protein (g)/Day: {mean_protein:.2f}\n" \
                 f"Mean Fat (g)/Day: {mean_fat:.2f}"
    axes[3].text(0.05, .3, stats_text, fontsize=8, verticalalignment='center')
    axes[3].axis('off')

    plt.tight_layout()

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