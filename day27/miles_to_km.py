import tkinter

MY_FONT = ("Arial", 14, "normal")

window = tkinter.Tk()

window.title("Miles to km converter")

window.minsize(width=300, height=200)

window.config(padx=50, pady=50)


def button_clicked():
    miles = entry.get()
    kms = int(int(miles) * 1.60934)
    label_res["text"] = kms

# Labels
label_equal = tkinter.Label(text="is equal to", font=MY_FONT)
label_equal.grid(row=1, column=0)
label_km = tkinter.Label(text="Km", font=MY_FONT)
label_km.grid(row=1, column=2)
label_miles = tkinter.Label(text="Miles", font=MY_FONT)
label_miles.grid(row=0, column=2)
label_res = tkinter.Label(text="0", font=MY_FONT)
label_res.grid(row=1, column=1)
# Entry
entry = tkinter.Entry(width=20)
entry.grid(row=0, column=1)

# Button
button = tkinter.Button(text="Calculate", command=button_clicked)
button.grid(column=1, row=2)


window.mainloop()
