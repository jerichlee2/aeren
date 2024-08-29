import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Specify the path to the CSV file
file_path = '/Users/jerichlee/Documents/aeren/csv/scores.csv'

def load_and_plot(file_path):
    # Load the CSV file into a pandas dataframe
    diet_data = pd.read_csv(file_path)

    # Convert the 'Date' column to datetime
    diet_data['date'] = pd.to_datetime(diet_data['date'], format='%Y-%m-%d')

    # Plotting
    fig, axis = plt.subplots(1, 1, figsize=(10, 5))

    scores = diet_data['score']

    # Daily Caloric Intake
    axis.plot(scores, marker='o', linestyle='-', color='r', markersize=2, linewidth=0.5)
    axis.set_title('Scores', fontsize=3)
    axis.set_xlabel('')
    axis.set_ylabel('Score', fontsize=3)
    axis.tick_params(axis='both', which='major', labelsize=3)
    axis.set_xticks([])
    axis.grid(True)  # General grid enable

    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2, hspace=0.5)

    # Display plot in tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Create the main window
root = tk.Tk()
root.title("Scores")

# Load and plot the data from the specified file path
load_and_plot(file_path)

# Run the application
root.mainloop()