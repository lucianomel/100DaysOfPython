from tkinter import *
from tkinter import messagebox

import requests.exceptions
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
        title.grid(row=7, column=0, columnspan=4)
        self.window.title("Pixela image generator")

        if user:
            user_label = Label(self.window, text=f"User: {user}", font=("Ariel",20,"bold"))
            user_label.grid(row=0, column=2, columnspan=2)

        self.canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
        image_button = Button(text="Create image", padx=2, pady=2, font=("Ariel", 20, "italic"), bg="white",
                              command=self.show_image)
        # Buttons
        image_button.grid(row=5, column=1)
        add_pixel_button = Button(text="Add pixel", padx=2, pady=2, font=("Ariel", 20, "italic"), bg="white",
                                  command=self.add_pixel_today)
        add_pixel_button.grid(row=2, column=1)

        add_pixel_button = Button(text="Modify pixel", padx=2, pady=2, font=("Ariel", 20, "italic"), bg="white",
                                  command=self.modify_pixel)
        add_pixel_button.grid(row=3, column=1)

        delete_pixel_button = Button(text="Remove pixel", padx=2, pady=2, font=("Ariel", 20, "italic"), bg="white",
                                     command=self.delete_pixel)
        delete_pixel_button.grid(row=3, column=1)

        create_graph = Button(text="Create graph", padx=2, pady=2, font=("Ariel", 20, "italic"), bg="white",
                                     command=self.create_graph)
        create_graph.grid(row=1, column=1)

        self.graph_type_input = StringVar(self.window)

        self.graph_type_button_int = Radiobutton(text="int", variable=self.graph_type_input, value=True, width=10,
                                             command=self.radio_button_select_int)
        self.graph_type_button_float = Radiobutton(text="float", variable=self.graph_type_input, value=False, width=10,
                                             command=self.radio_button_select_float)
        self.graph_type_button_int.grid(row=4, column=3)
        self.graph_type_button_float.grid(row=4, column=4)

        # Labels
        date_label = Label(text="Date (Example 2023-01-20): ")
        date_label.grid(row=1, column=2)
        self.date = Entry(width=30)
        self.date.grid(row=1, column=3, columnspan=2)

        pixel_size = Label(text="Pixel Size (a number): ")
        pixel_size.grid(row=2, column=2)
        self.pixel_size = Entry(width=30)
        self.pixel_size.grid(row=2, column=3, columnspan=2)

        graph_name_label = Label(text="Graph name: ")
        graph_name_label.grid(row=3, column=2)
        self.graph_name_input = Entry(width=30)
        self.graph_name_input.grid(row=3, column=3, columnspan=2)

        graph_type_label = Label(text="Graph type: ")
        graph_type_label.grid(row=4, column=2)

        graph_units_label = Label(text="Graph units: ")
        graph_units_label.grid(row=5, column=2)
        self.graph_units_input = Entry(width=30)
        self.graph_units_input.grid(row=5, column=3, columnspan=2)

        # Graph List
        self.graphs_list = Listbox(width=20, height=3, selectborderwidth=5, listvariable=self.habit_tracker.graphs)
        for graph in self.habit_tracker.graphs:
            self.graphs_list.insert(END, graph["name"])
        self.graphs_list.grid(row=6, column=3, columnspan=2)

        self.graphs_list.bind("<<ListboxSelect>>", self.graphs_callback)

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
        self.canvas.grid(row=8, column=1, columnspan=4, padx=20, pady=20)
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

    def create_graph(self):
        g_name = self.graph_name_input.get().strip()
        g_type = str(self.graph_type_input).strip()
        g_units = self.graph_units_input.get().strip()
        # Validation
        if g_type == "PY_VAR0":
            messagebox.showinfo("Error", message="Missing selection of graph type")
            return
        if not g_name:
            messagebox.showinfo("Error", message="Missing graph name")
            return
        if not g_units:
            messagebox.showinfo("Error", message="Missing graph units")
            return

        #Api call
        try:
            print(f"Graph name: {g_name}. Graph type: {g_type}. Graph units: {g_units}")
            self.habit_tracker.create_graph(graph_name=g_name, graph_type=g_type, graph_units=g_type)
            self.clear_inputs()
            #Reset graphs in list
            self.graphs_list.config(listvariable=self.habit_tracker.graphs)
            messagebox.showinfo(message=f"Graph created. Graph name: {g_name}. Graph type: {g_type}. Graph units: {g_units}")
        except requests.exceptions.HTTPError as e:
            print(e)

    def add_pixel_today(self):
        g_id = self.current_graph_id
        print(g_id)
        pixel_size = self.pixel_size.get().strip()
        # Validation
        if not g_id:
            messagebox.showinfo("Error",message="Missing graph selection")
            return
        if not pixel_size:
            messagebox.showinfo("Error",message="Missing quantity")
            return
        print(self.habit_tracker.add_pixel_today(graph_id=g_id, qty=pixel_size))
        self.clear_inputs()

    def delete_pixel(self):
        g_id = self.current_graph_id
        date = "".join(str(self.date).strip().split("-"))
        # Validation
        if not g_id:
            messagebox.showinfo("Error", message="Missing graph selection")
            return
        if not date:
            messagebox.showinfo("Error", message="Missing date")
            return
        print(self.habit_tracker.delete_pixel(graph_id=g_id, date=date))
        self.clear_inputs()

    def modify_pixel(self):
        g_id = self.current_graph_id
        date = "".join(str(self.date).strip().split("-"))
        pixel_size = self.pixel_size.get().strip()
        # Validation
        if not g_id:
            messagebox.showinfo("Error", message="Missing graph selection")
            return
        if not date:
            messagebox.showinfo("Error", message="Missing date")
            return
        if not pixel_size:
            messagebox.showinfo("Error", message="Missing quantity")
            return
        self.habit_tracker.modify_pixel(date=date, graph_id=g_id, pixel_qty=pixel_size)
        self.clear_inputs()

    def radio_button_select_int(self):
        self.graph_type_input = "int"

    def radio_button_select_float(self):
        self.graph_type_input = "float"

    def clear_inputs(self):
        self.graph_name_input.delete(0, END)
        self.graph_units_input.delete(0, END)
        self.date.delete(0, END)
        self.pixel_size.delete(0, END)


ui = UI()
