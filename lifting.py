import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_graph(root):
    # Load the CSV file
    df = pd.read_csv('/Users/jerichlee/Documents/aeren/csv/lifting.csv')
    
    # Convert the 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y')

    # Filter out rows where 'Active Zone Minutes' is missing
    df = df.dropna(subset=['Active Zone Minutes'])

    # Group by Date and Workout Type, summing Active Zone Minutes
    df_grouped = df.groupby(['Date', 'Workout Type'])['Active Zone Minutes'].sum().reset_index()

    # Set colors for workout types
    color_map = {
        'Push': 'red',
        'Pull': 'blue',
        'Legs': 'green'
    }

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    for workout_type in df_grouped['Workout Type'].unique():
        subset = df_grouped[df_grouped['Workout Type'] == workout_type]
        ax.bar(subset['Date'], subset['Active Zone Minutes'], color=color_map[workout_type], label=workout_type)

    # Formatting the plot
    ax.set_xlabel('Date')
    ax.set_ylabel('Active Zone Minutes')
    ax.set_title('Active Zone Minutes by Workout Type')
    ax.legend()
    ax.grid(True)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    fig.autofmt_xdate()

    # Embedding the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Tkinter setup
root = tk.Tk()
root.title("Lifting")

# Run the plot function
plot_graph(root)

# Start the Tkinter event loop
root.mainloop()