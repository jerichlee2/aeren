import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_graph(root):
    # Load the lifting CSV file
    df_lifting = pd.read_csv('/Users/jerichlee/Documents/aeren/csv/lifting.csv')
    
    # Convert the 'Date' column to datetime for lifting data
    df_lifting['Date'] = pd.to_datetime(df_lifting['Date'], format='%Y-%m-%d')

    # Set colors for workout types
    color_map = {
        'push': 'red',
        'pull': 'blue',
        'legs': 'green',
        'none': 'grey'
    }

    # Replace missing 'Active Zone Minutes' with zero
    df_lifting['Active Zone Minutes'] = df_lifting['Active Zone Minutes'].fillna(0)

    # Add a small constant to ensure bars are visible even for zero values
    small_constant = 5
    df_lifting['Adjusted Active Zone Minutes'] = df_lifting['Active Zone Minutes'] + small_constant

    # Group by Date and Workout Type, summing Adjusted Active Zone Minutes
    df_grouped = df_lifting.groupby(['Date', 'Workout Type'])['Adjusted Active Zone Minutes'].sum().reset_index()

    # Load the body CSV file
    df_body = pd.read_csv('/Users/jerichlee/Documents/aeren/csv/body.csv')
    
    # Convert the 'Date' column to datetime for body data
    df_body['Date'] = pd.to_datetime(df_body['Date'], format='%Y-%m-%d')

    # Get the common date range for all plots
    min_date = min(df_grouped['Date'].min(), df_body['Date'].min())
    max_date = max(df_grouped['Date'].max(), df_body['Date'].max())

    # Plotting
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 18))

    # Plot Active Zone Minutes
    for workout_type in df_grouped['Workout Type'].unique():
        subset = df_grouped[df_grouped['Workout Type'] == workout_type]
        ax1.bar(subset['Date'], subset['Adjusted Active Zone Minutes'], color=color_map[workout_type], label=workout_type)

    # Formatting the Active Zone Minutes plot
    # ax1.set_xlabel('Date', fontsize=4)
    ax1.set_ylabel('Active Zone Minutes', fontsize=3)
    ax1.set_title('Active Zone Minutes by Workout Type', fontsize=3)
    ax1.legend(loc='best',fontsize=3)
    # ax1.grid(True, axis='y')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax1.set_xlim([min_date, max_date])
    ax1.tick_params(axis='both', which='major', labelsize=3)
    ax1.tick_params(axis='x', rotation=90)
    ax1.set_xticks([])

    # Plot Body Fat Percentage
    ax2.plot(df_body['Date'], df_body['bodyfat percentage'], color='purple', marker='o', linestyle='-', label='Bodyfat %', markersize=2, linewidth=0.5)
    # ax2.set_xlabel('Date', fontsize=4)
    ax2.set_ylabel('Bodyfat Percentage', fontsize=3)
    ax2.set_title('Bodyfat Percentage Over Time', fontsize=3)
    ax2.grid(True, axis='y')
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    ax2.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax2.set_xlim([min_date, max_date])
    ax2.tick_params(axis='both', which='major', labelsize=3)
    ax2.tick_params(axis='x', rotation=90)
    ax2.set_xticks([])

    # Plot Body Weight
    ax3.plot(df_body['Date'], df_body['bodyweight'], color='orange', marker='o', linestyle='-', label='Bodyweight', markersize=2, linewidth=0.5)
    ax3.set_xlabel('Date', fontsize=4)
    ax3.set_ylabel('Bodyweight (lbs)', fontsize=3)
    ax3.set_title('Bodyweight Over Time', fontsize=3)
    ax3.grid(True, axis='y')
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    ax3.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax3.set_xlim([min_date, max_date])
    ax3.tick_params(axis='both', which='major', labelsize=3)
    ax3.tick_params(axis='x', rotation=90)
    
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2, hspace=0.5)


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