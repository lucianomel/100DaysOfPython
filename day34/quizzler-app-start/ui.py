from tkinter import *
from tkinter import messagebox

from quiz_brain import QuizBrain
from data import categories

THEME_COLOR = "#375362"


class QuizInterface:
    def __init__(self, quiz: QuizBrain):
        # Init window
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(bg=THEME_COLOR, pady=20, padx=20)
        # Init canvas
        self.canvas = Canvas(height=250, width=300)
        self.quiz_question = self.canvas.create_text(150, 125, font=("Arial", 20, "italic"), width=280)  # Text display problem -> width
        self.canvas.grid(row=1, column=0, columnspan=2)
        # Init buttons
        right_img = PhotoImage(file="./images/true.png")
        self.right_button = Button(image=right_img, highlightthickness=0, command=self.true_pressed)
        self.right_button.grid(row=2, column=0, pady=(20, 0))
        wrong_img = PhotoImage(file='./images/false.png')
        self.wrong_button = Button(image=wrong_img, highlightthickness=0, command=self.false_pressed)
        self.wrong_button.grid(row=2, column=1, pady=(20, 0))
        # Init score label
        self.score_label = Label(text=f"Score: 0", bg=THEME_COLOR, fg="white")
        self.score_label.grid(row=0, column=1, pady=20, padx=20)
        # Init list of categories
        categories_var = Variable(value=categories)
        self.categories_list = Listbox(master=self.window, selectmode=BROWSE, height=25, width=40,
                                       listvariable=categories_var)
        self.categories_list.grid(rowspan=3, row=0, column=2, padx=50)
        self.categories_list.bind('<<ListboxSelect>>', self.change_topic)

        self.quiz = quiz
        # First question
        self.get_next_question()
        # Start game
        self.window.mainloop()

    def get_next_question(self):
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            self.right_button.config(state="active")
            self.wrong_button.config(state="active")
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.quiz_question, text=q_text)
            self.score_label.config(text=f"Score: {self.quiz.score}")
        else:
            self.canvas.itemconfig(self.quiz_question, text="You've reached the end of the quiz")
            self.right_button.config(state="disabled")
            self.wrong_button.config(state="disabled")

    def true_pressed(self):
        self.give_feedback(self.quiz.check_answer("True"))

    def false_pressed(self):
        self.give_feedback(self.quiz.check_answer("False"))

    def give_feedback(self, is_right):
        if is_right:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        self.window.after(1000, func=self.get_next_question)

    def change_topic(self, event):
        # get all selected indices
        selected_index = self.categories_list.curselection()[0]
        # get selected items
        selected_category = self.categories_list.get(selected_index)
        can_modify_category = self.quiz.set_game_category(selected_category)
        if can_modify_category:
            self.get_next_question()
        else:
            messagebox.showerror(message="Server error, please try another category", title="server error")
