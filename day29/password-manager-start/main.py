from tkinter import *
from tkinter import messagebox
from random import choice,randint,shuffle
import pyperclip
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = randint(8, 10)
    nr_symbols = randint(2, 4)
    nr_numbers = randint(2, 4)

    password_letter_list = [choice(letters) for _ in range(nr_letters)]

    password_symbols_list = [choice(symbols) for _ in range(nr_symbols)]

    password_numbers_list = [choice(numbers) for _ in range(nr_numbers)]

    password_list = password_numbers_list+password_symbols_list+password_letter_list

    shuffle(password_list)

    password = "".join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get().strip()
    password = password_entry.get().strip()
    email = user_entry.get().strip()
    if not email or not password or not website:
        messagebox.showinfo(title="Oops",message="Don't leave fields empty!")
        return
    is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email} \nPassword: {password} \n is ok to save?")
    if is_ok:
        with open("data.txt", "a") as password_file:
            password_file.write(f"{website} | {email} | {password}\n")
        # Clear fields
        website_entry.delete(0, END)
        password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.config(padx=20, pady=20)
window.title("Password Manager")

lock_img = PhotoImage(file="logo.png")
canvas = Canvas(window, width=200, height=200)
canvas.create_image(0, 0, image=lock_img, anchor="nw")
canvas.grid(row=0, column=1)

website_label = Label(text="Website")
website_label.grid(row=1, column=0)
user_label = Label(text="Email/Username")
user_label.grid(row=2, column=0)
password_label = Label(text="Password")
password_label.grid(row=3, column=0)

website_entry = Entry(width=51)
website_entry.focus()
website_entry.grid(row=1, column=1, columnspan=2)
user_entry = Entry(width=51)
user_entry.insert(0, "hello@gmail.com")
user_entry.grid(row=2, column=1, columnspan=2)

password_entry = Entry(width=25)
password_entry.grid(row=3, column=1)

gen_psw_button = Button(text="Generate Password", width=22, command=generate_password)
gen_psw_button.grid(row=3, column=2)

add_button = Button(text="Add", width=48, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
