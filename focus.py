import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def load_csv(file_path):
    df = pd.read_csv(file_path)
    return df

def preprocess_books_data(df, file_path):
    df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)
    last_date = df['Date'].max().date()
    today = pd.to_datetime('today').date()
    missing_dates = pd.date_range(start=last_date, end=today)[1:]

    missing_data = pd.DataFrame({
        'Date': missing_dates,
        'Start Time': [pd.NaT] * len(missing_dates),
        'End Time': [pd.NaT] * len(missing_dates),
        'Duration': [0] * len(missing_dates)  # This will be calculated later
    })

    df = pd.concat([df, missing_data], ignore_index=True)
    df = df.sort_values(by='Date').reset_index(drop=True)
    
    # Calculate Duration in a separate DataFrame
    duration_df = df.copy()
    duration_df['Duration'] = (pd.to_datetime(duration_df['End Time'], infer_datetime_format=True) -
                               pd.to_datetime(duration_df['Start Time'], infer_datetime_format=True)).dt.total_seconds() / 3600

    # Prepare data for plotting
    daily_work = duration_df.groupby(duration_df['Date'].dt.date)['Duration'].sum().reset_index()
    daily_work['Date'] = pd.to_datetime(daily_work['Date'], infer_datetime_format=True)

    date_range = pd.date_range(start=daily_work['Date'].min(), end=daily_work['Date'].max())
    daily_work = daily_work.set_index('Date').reindex(date_range, fill_value=0).reset_index()
    daily_work.columns = ['Date', 'Duration']

    # Remove Duration before saving the DataFrame
    df = df.drop(columns=['Duration'])
    df.to_csv(file_path, index=False)

    return daily_work

def preprocess_deepwork_data(df):
    df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)
    df['Start Time'] = pd.to_datetime(df['Start Time'], infer_datetime_format=True)
    df['End Time'] = pd.to_datetime(df['End Time'], infer_datetime_format=True)
    df['Duration'] = (df['End Time'] - df['Start Time']).dt.total_seconds() / 3600

    daily_work = df.groupby(df['Date'].dt.date)['Duration'].sum().reset_index()
    daily_work['Date'] = pd.to_datetime(daily_work['Date'])

    date_range = pd.date_range(start=daily_work['Date'].min(), end=pd.to_datetime('today'))
    daily_work = daily_work.set_index('Date').reindex(date_range, fill_value=0).reset_index()
    daily_work.columns = ['Date', 'Duration']

    return daily_work

def plot_data(daily_books, daily_deepwork, root):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
    
    ax1.plot(daily_books['Date'], daily_books['Duration'], marker='o', linestyle='-', color='blue')
    ax1.set_xlabel('Date', fontsize=5)
    ax1.set_ylabel('Total Duration (hours)', fontsize=5)
    ax1.set_title('Total Reading Time Per Day', fontsize=5)
    ax1.grid(True)
    ax1.set_ylim(0, 12)
    ax1.tick_params(axis='x', rotation=90, labelsize=0)
    ax1.tick_params(axis='y', labelsize=5)
    
    ax2.plot(daily_deepwork['Date'], daily_deepwork['Duration'], marker='o', linestyle='-', color='green')
    ax2.set_xlabel('Date', fontsize=5)
    ax2.set_ylabel('Total Duration (hours)', fontsize=5)
    ax2.set_title('Total Deep Work Time Per Day', fontsize=5)
    ax2.grid(True)
    ax2.set_ylim(0, 12)
    ax2.tick_params(axis='x', rotation=90, labelsize=5)  # Display x-axis dates
    ax2.tick_params(axis='y', labelsize=5)
    
    plt.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

file_path_books = '/Users/jerichlee/Documents/aeren/csv/books.csv'
file_path_deepwork = '/Users/jerichlee/Documents/aeren/csv/deepwork.csv'

df_books = load_csv(file_path_books)
df_deepwork = load_csv(file_path_deepwork)

daily_books = preprocess_books_data(df_books, file_path_books)
daily_deepwork = preprocess_deepwork_data(df_deepwork)

root = Tk()
root.title("Focus")

plot_data(daily_books, daily_deepwork, root)

root.mainloop()