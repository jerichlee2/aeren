import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

# Default macronutrient goals
default_carb_goal = 200
default_protein_goal = 180
default_fat_goal = 40

# Current macronutrient goals
carb_goal = default_carb_goal
protein_goal = default_protein_goal
fat_goal = default_fat_goal

def create_pie_charts(data, carb_goal, protein_goal, fat_goal, plot_frame):
    daily_totals = data.groupby('Date')[['Carbs (g)', 'Protein (g)', 'Fat (g)']].sum().reset_index()

    # Clear the existing canvas if it exists
    for widget in plot_frame.winfo_children():
        widget.destroy()

    for index, row in daily_totals.iterrows():
        date = row['Date']
        total_carbs = row['Carbs (g)']
        total_proteins = row['Protein (g)']
        total_fats = row['Fat (g)']

        carb_percent = total_carbs / carb_goal * 100
        protein_percent = total_proteins / protein_goal * 100
        fat_percent = total_fats / fat_goal * 100

        def get_colors(percent):
            if percent > 100:
                return ['#FF6666']
            elif 95 <= percent <= 100:
                return ['#4CAF50', '#87CEEB']
            else:
                return ['#1E90FF', '#87CEEB']

        colors_carbs = get_colors(carb_percent)
        colors_proteins = get_colors(protein_percent)
        colors_fats = get_colors(fat_percent)

        fig, axs = plt.subplots(1, 3, figsize=(18, 6))

        if carb_percent > 100:
            axs[0].pie(
                [100],
                labels=[f'{carb_percent:.1f}%'],
                colors=['#FF6666'],
                startangle=90,
                wedgeprops=dict(width=0.3)
            )
        else:
            sizes_carbs = [min(carb_percent, 100), max(0, 100 - carb_percent)]
            axs[0].pie(
                sizes_carbs,
                autopct='%1.1f%%',
                startangle=90,
                pctdistance=0.85,
                colors=colors_carbs[:len(sizes_carbs)],
                wedgeprops=dict(width=0.3)
            )
        axs[0].set_title('Carbs')

        if protein_percent > 100:
            axs[1].pie(
                [100],
                labels=[f'{protein_percent:.1f}%'],
                colors=['#FF6666'],
                startangle=90,
                wedgeprops=dict(width=0.3)
            )
        else:
            sizes_proteins = [min(protein_percent, 100), max(0, 100 - protein_percent)]
            axs[1].pie(
                sizes_proteins,
                autopct='%1.1f%%',
                startangle=90,
                pctdistance=0.85,
                colors=colors_proteins[:len(sizes_proteins)],
                wedgeprops=dict(width=0.3)
            )
        axs[1].set_title('Proteins')

        if fat_percent > 100:
            axs[2].pie(
                [100],
                labels=[f'{fat_percent:.1f}%'],
                colors=['#FF6666'],
                startangle=90,
                wedgeprops=dict(width=0.3)
            )
        else:
            sizes_fats = [min(fat_percent, 100), max(0, 100 - fat_percent)]
            axs[2].pie(
                sizes_fats,
                autopct='%1.1f%%',
                startangle=90,
                pctdistance=0.85,
                colors=colors_fats[:len(sizes_fats)],
                wedgeprops=dict(width=0.3)
            )
        axs[2].set_title('Fats')

        for ax in axs:
            centre_circle = plt.Circle((0, 0), 0.70, fc='white')
            ax.add_artist(centre_circle)
            ax.axis('equal')

        plt.suptitle(f"Macronutrient Consumption for {date}")
    
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def refresh_plot():
    global carb_goal, protein_goal, fat_goal
    print(f"Refreshing plot with goals - Carbs: {carb_goal}, Proteins: {protein_goal}, Fats: {fat_goal}")
    data = pd.read_csv('diet_aeren_test.csv')
    create_pie_charts(data, carb_goal, protein_goal, fat_goal, plot_frame)

def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")

    ttk.Label(settings_window, text="Carbs (g)").pack()
    entry_carbs = ttk.Entry(settings_window)
    entry_carbs.pack()
    entry_carbs.insert(0, str(carb_goal))

    ttk.Label(settings_window, text="Proteins (g)").pack()
    entry_proteins = ttk.Entry(settings_window)
    entry_proteins.pack()
    entry_proteins.insert(0, str(protein_goal))

    ttk.Label(settings_window, text="Fats (g)").pack()
    entry_fats = ttk.Entry(settings_window)
    entry_fats.pack()
    entry_fats.insert(0, str(fat_goal))

    def save_settings():
        global carb_goal, protein_goal, fat_goal
        carb_goal = float(entry_carbs.get())
        protein_goal = float(entry_proteins.get())
        fat_goal = float(entry_fats.get())
        settings_window.destroy()
        # Update the goals display
        current_goals_label.config(text=f"Carbs: {carb_goal}g, Proteins: {protein_goal}g, Fats: {fat_goal}g")

    save_button = ttk.Button(settings_window, text="Save", command=save_settings)
    save_button.pack()

root = tk.Tk()
root.title("Macronutrient Goals")
root.state('zoomed')  # Make the window full screen

frame = ttk.Frame(root, padding="10")
frame.pack(fill=tk.BOTH, expand=True)

ttk.Label(frame, text="Current goals:").pack()
current_goals_label = ttk.Label(frame, text=f"Carbs: {carb_goal}g, Proteins: {protein_goal}g, Fats: {fat_goal}g")
current_goals_label.pack()

settings_button = ttk.Button(frame, text="Settings", command=open_settings)
settings_button.pack()

refresh_button = ttk.Button(frame, text="Refresh", command=refresh_plot)
refresh_button.pack()

plot_frame = ttk.Frame(root, padding="10")
plot_frame.pack(fill=tk.BOTH, expand=True)

# Load data and create pie charts at startup
data = pd.read_csv('diet_aeren_test.csv')
create_pie_charts(data, carb_goal, protein_goal, fat_goal, plot_frame)

root.mainloop()