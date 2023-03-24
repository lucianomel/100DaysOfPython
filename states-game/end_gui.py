import tkinter as tk
from tkinter import messagebox
import pandas as pd

def show_missing_states(states):
    # add states missing count
    states.insert(0, f"Count of provinces missing: {len(states)}")

    # Create the main window
    root = tk.Tk()
    root.title("Provinces Missing")

    # Set the size of the window
    root.geometry("400x400")

    # Create a listbox
    listbox = tk.Listbox(root, width=50, height=20)
    listbox.pack()

    # Add items to the listbox
    for item in states:
        listbox.insert(tk.END, item)

    if len(states) == 0:
        messagebox.showinfo("Game Finished", "You won! Congratulations!")
    else:
        messagebox.showinfo("Game Finished",
                            "You have some provinces to learn yet. Look at the csv file created and learn "
                            "them befor trying again!")
        # Save missed states
        df_missing_states = pd.DataFrame(states)
        df_missing_states.to_csv("states_to_learn.csv")

    # Run the main loop
    root.mainloop()
