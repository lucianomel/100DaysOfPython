#!/usr/bin/env python3
from tkinter import *
# ---------------------------- CONSTANTS ------------------------------- #
standard = [
# PINK
# RED
# GREEN
# YELLOW
    "#e2979c",
    "#e7305b",
    "#9bdeac",
    "#f7f5dd",
]
blue = [
    "#A5D7E8",
    "#0B2447",
    "#19376D",
    "#576CBC"
]
green = [
    "#EDF1D6",
    "#9DC08B",
    "#609966",
    "#40513B"
]
STANDARD_INDEX = 0
BLUE_INDEX = 1
GREEN_INDEX = 2
COLORS = [standard, blue, green]

FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None
pop_up = False
current_selected_pallet = 0
# ---------------------------- TIMER RESET ------------------------------- #


def theme_callback(event):
    global current_selected_pallet
    index_selection = event.widget.curselection()[0]
    current_selected_pallet = index_selection
    change_colors()


def change_colors():
    window.config(bg=COLORS[current_selected_pallet][3])
    canvas.config(bg=COLORS[current_selected_pallet][3], highlightthickness=0)
    title_label.config(fg=COLORS[current_selected_pallet][2],bg=COLORS[current_selected_pallet][3])
    check_label.config(bg=COLORS[current_selected_pallet][3], fg=COLORS[current_selected_pallet][2])


# ---------------------------- TIMER RESET ------------------------------- #

def toggle_pop_up():
    global pop_up
    pop_up = not pop_up

# ---------------------------- TIMER RESET ------------------------------- # 


def reset_timer():
    global reps
    window.after_cancel(timer)
    # 00:00
    canvas.itemconfig(timer_text, text="00:00")
    # title_label "Timer"
    title_label.config(text="Timer")
    # reset check_marks
    check_label.config(text="")
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- # 


def start_timer():
    global reps
    reps += 1
    work_secs = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if pop_up:
        window.withdraw()
        window.deiconify()

    if reps % 2 == 1:
        count_down(work_secs)
        title_label["text"] = "Work"
        title_label["fg"] = COLORS[current_selected_pallet][2]
    if reps % 8 == 0:
        count_down(long_break_sec)
        title_label["text"] = "Break"
        title_label["fg"] = COLORS[current_selected_pallet][0]
    elif reps % 2 == 0:
        count_down(short_break_sec)
        title_label["text"] = "Break"
        title_label["fg"] = COLORS[current_selected_pallet][1]

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 


def count_down(n):
    if n < 0:
        check_marks = ""
        work_sessions = reps//2
        for _ in range(work_sessions):
            check_marks += "✔"
        check_label["text"] = check_marks
        start_timer()
        return
    count_secs = n % 60
    if count_secs < 10:
        count_secs = f"0{count_secs}"
    count_min = n//60
    if count_min < 10:
        count_min = f'0{count_min}'
    global timer
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_secs}")
    timer = window.after(1000, count_down, n-1)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=COLORS[current_selected_pallet][3])


photo = PhotoImage(file="tomato.png")
canvas = Canvas(width=202, height=224, bg=COLORS[current_selected_pallet][3], highlightthickness=0)
canvas.create_image(100, 112, image=photo)
timer_text = canvas.create_text(103, 135, text="00:00", fill="white", font=(FONT_NAME, 24,"bold"))
canvas.grid(row=1, column=1)


# Timer title label
title_label = Label(text="Timer", fg=COLORS[current_selected_pallet][2], font=(FONT_NAME,30), bg=COLORS[current_selected_pallet][3])
title_label.grid(row=0, column=1)

# Start button
start_label = Button(text="start", command=start_timer)
start_label.grid(row=2, column=0)

# Restart button
restart_label = Button(text="restart", command=reset_timer)
restart_label.grid(row=2, column=2)

# Check label
check_label = Label(bg=COLORS[current_selected_pallet][3], fg=COLORS[current_selected_pallet][2])
check_label.grid(row=3, column=1)

# Popup
pop_up_button = Checkbutton(text="Popup", command=toggle_pop_up)
pop_up_button.grid(row=0, column=2)


# theme
theme_list = Listbox(width=20, height=3, selectborderwidth=5)

theme_list.insert(STANDARD_INDEX, "Standard")
theme_list.itemconfig(index=STANDARD_INDEX, selectbackground=COLORS[STANDARD_INDEX][0])
theme_list.insert(BLUE_INDEX, "Blue")
theme_list.itemconfig(index=BLUE_INDEX, selectbackground=COLORS[BLUE_INDEX][0])
theme_list.insert(GREEN_INDEX,"Green")
theme_list.itemconfig(index=GREEN_INDEX, selectbackground=COLORS[GREEN_INDEX][0])
theme_list.grid(row=0, column=3)

theme_list.bind("<<ListboxSelect>>", theme_callback)

window.mainloop()

# dynamic typing

