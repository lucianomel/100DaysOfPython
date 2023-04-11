from tkinter import *
from tkinter import messagebox
from cairosvg import svg2png
from habit_tracker import HabitTracker


class UI:
    def __init__(self, login=True,h_t=HabitTracker(), user=None):
        self.habit_tracker = h_t
        if login:
            self.window2 = Tk()
            self.login_form()

        self.window = Tk()
        self.window.config(pady=20, padx=20)
        title = Label(text="Tap on the buttons to create your image")
        title.grid(row=0, column=0)
        self.window.title("Pixela image generator")

        if user:
            user_label = Label(self.window, text=f"User: {user}", font=("Ariel",20,"bold"))
            user_label.grid(row=0, column=2, columnspan=2)

        self.canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
        image_button = Button(text="Create image", padx=2, pady=2, font=("Ariel", 20, "italic"), bg="white",
                              command=self.show_image)
        # Buttons
        image_button.grid(row=1, column=1)
        add_pixel_button = Button(text="Add pixel", padx=2, pady=2, font=("Ariel", 20, "italic"), bg="white",
                                  command=self.add_pixel)
        add_pixel_button.grid(row=2, column=1)

        add_pixel_button = Button(text="Modify pixel", padx=2, pady=2, font=("Ariel", 20, "italic"), bg="white",
                                  command=self.modify_pixel)
        add_pixel_button.grid(row=3, column=1)

        delete_pixel_button = Button(text="Remove pixel", padx=2, pady=2, font=("Ariel", 20, "italic"), bg="white",
                                     command=self.delete_pixel)
        delete_pixel_button.grid(row=3, column=1)

        # Labels
        date_label = Label(text="Date (Example 2023-01-01): ")
        date_label.grid(row=1, column=2)
        self.date = Entry(width=30)
        self.date.grid(row=1, column=3)

        pixel_size = Label(text="Pixel Size (a number): ")
        pixel_size.grid(row=2, column=2)
        self.pixel_size = Entry(width=30)
        self.pixel_size.grid(row=2, column=3)

        # Graph List
        graphs_list = Listbox(width=20, height=3, selectborderwidth=5, listvariable=self.habit_tracker.graphs)
        for graph in self.habit_tracker.graphs:
            graphs_list.insert(0, graph["name"])
        graphs_list.grid(row=3, column=3)

        graphs_list.bind("<<ListboxSelect>>", self.graphs_callback)

        self.current_graph_id = None

    def graphs_callback(self, event):
        index_selection = event.widget.curselection()[0]
        current_selected_graph = index_selection
        graph_id = self.habit_tracker.graphs[index_selection]["id"]
        self.current_graph_id = graph_id
        print(graph_id)

    def show_image(self):
        with open("image.svg") as image_file:
            image_string = image_file.read()
            svg2png(bytestring=image_string, write_to='output.png')
        image = PhotoImage(file="./output.png")
        self.canvas.config(width=image.width(), height=image.height())
        self.canvas.create_image(0, 0, image=image, anchor="nw")
        self.canvas.grid(row=1, column=0, rowspan=4, padx=20, pady=20)
        self.window.mainloop()

    def login_open_main_window(self):
        input_user = self.log_in_entry.get().strip()
        if self.habit_tracker.start(input_user):
            #Login successful
            self.window2.destroy()
            self = UI(login=False, h_t=self.habit_tracker, user=input_user)
        else:
            messagebox.showerror("Please try again")

    def login_form(self):
        self.window2.config(pady=20, padx=20)
        self.log_in_entry = Entry(self.window2, bg="white")
        log_in_label = Label(self.window2, text="Log in", font=("Ariel", 60, "italic"))
        log_in_user_label = Label(self.window2, text="Username: ", font=("Ariel", 20, "normal"))
        log_in_button = Button(self.window2, text="Log in", command=self.login_open_main_window)
        log_in_button.grid(row=3,column=0, columnspan=2)
        log_in_label.grid(row=0, columnspan=2, column=0)
        log_in_user_label.grid(row=1, column=0)
        self.log_in_entry.grid(row=1, column=1)
        self.window2.mainloop()

    def add_pixel(self):
        self.habit_tracker.add_pixel_today()

    def delete_pixel(self):
        self.habit_tracker.delete_pixel()

    def modify_pixel(self):
        self.habit_tracker.modify_pixel()


ui = UI()
