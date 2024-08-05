import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, Label
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def load_csv(file_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    return df

def preprocess_data(df):
    # Convert the 'Date', 'Start Time', and 'End Time' columns to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Calculate the duration of each deep work session
    df['Duration'] = (df['End Time'] - df['Start Time']).dt.total_seconds() / 3600

    # Aggregate the total duration per day
    daily_work = df.groupby(df['Date'].dt.date)['Duration'].sum().reset_index()
    daily_work['Date'] = pd.to_datetime(daily_work['Date'])

    return daily_work

def plot_deep_work(daily_work, root):
    # Plot the total duration of deep work sessions per day
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(daily_work['Date'], daily_work['Duration'], marker='o', linestyle='-')
    ax.set_xlabel('Date', fontsize=5)
    ax.set_ylabel('Total Duration (hours)', fontsize=5)
    ax.set_title('Total Reading Time Per Day', fontsize=5)
    ax.grid(True)
    plt.xticks(rotation=90)
    plt.xticks(fontsize=5)  # X-axis tick labels font size
    plt.yticks(fontsize=5)  # Y-axis tick labels font size

    plt.tight_layout()

    # Display the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Path to the CSV file
file_path = '/Users/jerichlee/Documents/aeren/csv/books.csv'

# Load and preprocess data
df = load_csv(file_path)
daily_work = preprocess_data(df)

# Create the main window
root = Tk()
root.title("Books")

# # Add a label to provide instructions
# instructions = Label(root, text="Deep Work Log Analysis")
# instructions.pack(pady=10)

# Plot the data
plot_deep_work(daily_work, root)

# Run the Tkinter event loop
root.mainloop()