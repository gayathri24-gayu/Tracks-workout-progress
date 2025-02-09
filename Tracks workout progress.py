import sqlite3
import logging
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import Tk, Label, Entry, Button, messagebox

# Configure logging
logging.basicConfig(filename="workout_log.txt", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

def create_database():
    conn = sqlite3.connect("workout_tracker.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS workout_history 
                      (id INTEGER PRIMARY KEY, exercise TEXT, reps INTEGER, sets INTEGER, weight REAL)''')
    conn.commit()
    conn.close()

def log_workout(exercise, reps, sets, weight):
    try:
        conn = sqlite3.connect("workout_tracker.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO workout_history (exercise, reps, sets, weight) VALUES (?, ?, ?, ?)",
                       (exercise, reps, sets, weight))
        conn.commit()
        conn.close()
        logging.info(f"Logged workout: {exercise}, Reps: {reps}, Sets: {sets}, Weight: {weight}")
        return "✅Workout logged successfully!"
    except Exception as e:
        logging.error(f"Error logging workout: {e}")
        return "Error logging workout."

def generate_report():
    try:
        conn = sqlite3.connect("workout_tracker.db")
        df = pd.read_sql_query("SELECT * FROM workout_history", conn)
        conn.close()
        df.to_csv("workout_report.csv", index=False)
        logging.info("Generated workout report.")
        return "Report generated successfully!"
    except Exception as e:
        logging.error(f"Error generating report: {e}")
        return "Error generating report."

def plot_progress():
    try:
        conn = sqlite3.connect("workout_tracker.db")
        df = pd.read_sql_query("SELECT * FROM workout_history", conn)
        conn.close()
        if df.empty:
            return "No data available for visualization."
        
        plt.figure(figsize=(10, 5))
        for exercise in df['exercise'].unique():
            subset = df[df['exercise'] == exercise]
            plt.plot(subset.index, subset['weight'], marker='o', label=exercise)
        plt.xlabel("Workout Session")
        plt.ylabel("Weight (kg)")
        plt.title("️⃣ Workout Progress Over Time")
        plt.legend()
        plt.show()
        logging.info("Plotted workout progress.")
    except Exception as e:
        logging.error(f"Error plotting progress: {e}")
        return "Error plotting progress."

def gui_app():
    root = Tk()
    root.title("Workout Tracker")
    
    Label(root, text="💪💪Exercise").grid(row=0, column=0)
    Label(root, text="🏋Reps").grid(row=1, column=0)
    Label(root, text="🔥Sets").grid(row=2, column=0)
    Label(root, text="Weight (kg)").grid(row=3, column=0)
    
    exercise_entry = Entry(root)
    reps_entry = Entry(root)
    sets_entry = Entry(root)
    weight_entry = Entry(root)
    
    exercise_entry.grid(row=0, column=1)
    reps_entry.grid(row=1, column=1)
    sets_entry.grid(row=2, column=1)
    weight_entry.grid(row=3, column=1)
    
    def submit():
        msg = log_workout(exercise_entry.get(), int(reps_entry.get()), int(sets_entry.get()), float(weight_entry.get()))
        messagebox.showinfo("Workout Log👋👋👋", msg)
    
    Button(root, text="Log Workout", command=submit).grid(row=4, column=0, columnspan=2)
    Button(root, text="Generate Report", command=lambda: messagebox.showinfo("Report", generate_report())).grid(row=5, column=0, columnspan=2)
    Button(root, text="Plot Progress", command=plot_progress).grid(row=6, column=0, columnspan=2)
    
    root.mainloop()

if __name__ == "__main__":
    create_database()
    gui_app()
