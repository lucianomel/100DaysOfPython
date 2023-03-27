import tkinter

window = tkinter.Tk()

window.title("My first GUI program")

window.minsize(width=500, height=300)

window.config(padx=100, pady=200)


def button_clicked():
    my_label["text"] = input.get()


#Label
my_label = tkinter.Label(text="I am a label",font=("Arial", 24, "normal"))
my_label["text"] = "New text"
# geometry management system
my_label.grid(column=0, row=0)
my_label.config(padx=50, pady=50)

#Button
button = tkinter.Button(text="Click me", command=button_clicked)
button.grid(column=1, row=1)

# Entry
input = tkinter.Entry(width=20)
input.grid(row=2, column=3)

# Button 2
button2 = tkinter.Button(text="Click me 2")
button2.grid(column=2, row=0)


#Layout and positioning - different layout managers -> pack place and grid
# Place: precise
# Grid: Imagine your program is a grid, row and columns
# Cant mix grid and pack

# Padding


window.mainloop()
