import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def load_csv(file_path):
    df = pd.read_csv(file_path)
    return df

def preprocess_books_data(df):
    df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)
    df['Start Time'] = pd.to_datetime(df['Start Time'], format='%I:%M %p', errors='coerce')
    df['End Time'] = pd.to_datetime(df['End Time'], format='%I:%M %p', errors='coerce')
    
    df['Duration'] = (df['End Time'] - df['Start Time']).dt.total_seconds() / 3600
    df.loc[df['Duration'] < 0, 'Duration'] += 24  # Adjust for overnight time spans

    daily_work = df.groupby(df['Date'].dt.date)['Duration'].sum().reset_index()
    daily_work['Date'] = pd.to_datetime(daily_work['Date'])

    date_range = pd.date_range(start=daily_work['Date'].min(), end=pd.to_datetime('today'))
    daily_work = daily_work.set_index('Date').reindex(date_range, fill_value=0).reset_index()
    daily_work.columns = ['Date', 'Duration']

    return daily_work

def preprocess_deepwork_data(df):
    df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)
    df['Start Time'] = pd.to_datetime(df['Start Time'], format='%I:%M %p', errors='coerce')
    df['End Time'] = pd.to_datetime(df['End Time'], format='%I:%M %p', errors='coerce')
    
    df['Duration'] = (df['End Time'] - df['Start Time']).dt.total_seconds() / 3600
    df.loc[df['Duration'] < 0, 'Duration'] += 24  # Adjust for overnight time spans

    daily_work = df.groupby(df['Date'].dt.date)['Duration'].sum().reset_index()
    daily_work['Date'] = pd.to_datetime(daily_work['Date'])

    date_range = pd.date_range(start=daily_work['Date'].min(), end=pd.to_datetime('today'))
    daily_work = daily_work.set_index('Date').reindex(date_range, fill_value=0).reset_index()
    daily_work.columns = ['Date', 'Duration']

    return daily_work

def preprocess_calm_data(df):
    df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)
    df['Start Time'] = pd.to_datetime(df['Start Time'], format='%I:%M %p', errors='coerce')
    df['End Time'] = pd.to_datetime(df['End Time'], format='%I:%M %p', errors='coerce')
    
    df['Duration'] = (df['End Time'] - df['Start Time']).dt.total_seconds() / 3600
    df.loc[df['Duration'] < 0, 'Duration'] += 24  # Adjust for overnight time spans

    daily_work = df.groupby(df['Date'].dt.date)['Duration'].sum().reset_index()
    daily_work['Date'] = pd.to_datetime(daily_work['Date'])

    date_range = pd.date_range(start=daily_work['Date'].min(), end=pd.to_datetime('today'))
    daily_work = daily_work.set_index('Date').reindex(date_range, fill_value=0).reset_index()
    daily_work.columns = ['Date', 'Duration']

    return daily_work

def plot_data(daily_books, daily_deepwork, daily_calm, root):
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10))
    
    # Plot for Total Reading Time Per Day
    ax1.plot(daily_books['Date'], daily_books['Duration'], marker='o', linestyle='-', color='blue', markersize=2, linewidth=0.5)
    ax1.set_ylabel('Total Duration (hours)', fontsize=3)
    ax1.set_title('Total Reading Time Per Day', fontsize=3)
    ax1.grid(True, axis='y')
    ax1.set_ylim(0, 12)
    ax1.set_xticks(daily_books['Date'])
    ax1.set_xticklabels(daily_books['Date'].dt.strftime('%Y-%m-%d'), rotation=90, fontsize=0)
    ax1.set_xticks([])
    ax1.tick_params(axis='y', labelsize=3)
    
    # Plot for Total Deep Work Time Per Day
    ax2.plot(daily_deepwork['Date'], daily_deepwork['Duration'], marker='o', linestyle='-', color='green', markersize=2, linewidth=0.5)
    ax2.set_ylabel('Total Duration (hours)', fontsize=3)
    ax2.set_title('Total Deep Work Time Per Day', fontsize=3)
    ax2.grid(True, axis='y')
    ax2.set_ylim(0, 12)
    ax2.set_xticks(daily_deepwork['Date'])
    ax2.set_xticklabels(daily_deepwork['Date'].dt.strftime('%Y-%m-%d'), rotation=90, fontsize=0)
    ax2.set_xticks([])
    ax2.tick_params(axis='y', labelsize=3)

    # Plot for Total Calm Time Per Day
    ax3.plot(daily_calm['Date'], daily_calm['Duration'], marker='o', linestyle='-', color='orange', markersize=2, linewidth=0.5)
    ax3.set_xlabel('Date', fontsize=3)
    ax3.set_ylabel('Total Duration (hours)', fontsize=3)
    ax3.set_title('Total Calm Time Per Day', fontsize=3)
    ax3.grid(True, axis='y')
    ax3.set_ylim(0, 12)
    ax3.set_xticks(daily_calm['Date'])
    ax3.set_xticklabels(daily_calm['Date'].dt.strftime('%m/%d'), rotation=90, fontsize=3)
    ax3.tick_params(axis='y', labelsize=3)
    
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2, hspace=0.5)

file_path_books = '/Users/jerichlee/Documents/aeren/csv/books.csv'
file_path_deepwork = '/Users/jerichlee/Documents/aeren/csv/deepwork.csv'
file_path_calm = '/Users/jerichlee/Documents/aeren/csv/calm.csv'

df_books = load_csv(file_path_books)
df_deepwork = load_csv(file_path_deepwork)
df_calm = load_csv(file_path_calm)

daily_books = preprocess_books_data(df_books)
daily_deepwork = preprocess_deepwork_data(df_deepwork)
daily_calm = preprocess_calm_data(df_calm)

root = Tk()
root.title("Focus")

plot_data(daily_books, daily_deepwork, daily_calm, root)

root.mainloop()