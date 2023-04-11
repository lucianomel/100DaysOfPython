from tkinter import *
from cairosvg import svg2png
from habit_tracker import HabitTracker


class UI:
    def __init__(self):
        self.habit_tracker = HabitTracker()
        self.window = Tk()
        self.window.title("Pixela image generator")
        title = Label(text="Tap on the buttons to create your image")
        title.grid(row=0, column=0)

        self.canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
        image_button = Button(text="Create image", padx=2, pady=2, font=("Ariel", 20, "italic"), bg="white",
                              command=self.show_image)
        image_button.grid(row=1, column=1)
        add_pixel_button = Button(text="Add pixel", padx=2, pady=2, font=("Ariel", 20, "italic"), bg="white",
                                  command=self.add_pixel)
        add_pixel_button.grid(row=2, column=1)

        add_pixel_button = Button(text="Modify pixel", padx=2, pady=2, font=("Ariel", 20, "italic"), bg="white",
                                  command=self.modify_pixel)
        add_pixel_button.grid(row=3, column=1)

        date_label = Label(text="Date: ")
        date_label.grid(row=0, column=2)
        self.date = Entry(width=30)
        self.date.grid(row=0, column=3)

        pixel_size = Label(text="Pixel Size: ")
        pixel_size.grid(row=1, column=2)
        self.pixel_size = Entry(width=30)
        self.pixel_size.grid(row=1, column=3)

        delete_pixel_button = Button(text="Remove pixel", padx=2, pady=2, font=("Ariel", 20, "italic"), bg="white",
                                     command=self.delete_pixel)
        delete_pixel_button.grid(row=3, column=1)
        self.window.mainloop()

    def show_image(self):
        with open("image.svg") as image_file:
            image_string = image_file.read()
            svg2png(bytestring=image_string, write_to='output.png')
        image = PhotoImage(file="./output.png")
        self.canvas.config(width=image.width(), height=image.height())
        self.canvas.create_image(0, 0, image=image, anchor="nw")
        self.canvas.grid(row=1, column=0, rowspan=4, padx=20, pady=20)
        self.window.mainloop()

    def add_pixel(self):
        HabitTracker.add_pixel_today()

    def delete_pixel(self):
        pass

    def modify_pixel(self):
        pass


ui = UI()
