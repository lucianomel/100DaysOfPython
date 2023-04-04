from tkinter import *
import pandas as pd
from random import randint, choice
BACKGROUND_COLOR = "#B1DDC6"
front = True

DICT_FILE_NAME = "data/italian_spanish.csv"



#-------------SAVE PROGRESS----------------#


def start_words():
    """Initialize df and file with words that can come up"""
    global df
    """"If words_to_learn does not exist, it creates it and fills it with every word"""
    df = pd.read_csv(DICT_FILE_NAME)
    try:
        file = open("data/words")
        file.close()
    except FileNotFoundError:
        with open("data/words", "w") as file:
            file.write("italian,spanish\n")
            for i, content in df.iterrows():
                file.write(f"{content['italian']},{content['spanish']}\n")
    load_words()


def load_words():
    global df
    #Load words to learn from previous games
    try:
        with open("data/words_to_learn") as file:
            df = pd.read_csv(file)
    except FileNotFoundError:
        df = pd.read_csv("data/words")
    if df.empty:
        df = pd.read_csv("data/words")


def delete_from_df():
    global df_index,df
    df.drop(df_index, inplace=True)

def delete_from_words_file():
    """Removes from 'words' file the current word"""
    words = get_random_words()
    random_words_line = f"{words[0]},{words[1]}\n"
    #Get every word
    with open("data/words", "r") as file:
        lines = file.readlines()
    #Rewrite every line except random_words_line
    with open("data/words", "w") as file:
        for line in lines:
            if line == random_words_line:
                pass
            else:
                file.write(line)


def delete_from_words_to_learn():
    words = get_random_words()
    random_words_line = f"{words[0]},{words[1]}\n"
    # Get every word
    try:
        with open("data/words_to_learn", "r") as file:
            lines = file.readlines()
        # Rewrite every line except random_words_line
        with open("data/words_to_learn", "w") as file:
            for line in lines:
                if line == random_words_line:
                    pass
                else:
                    file.write(line)
    except FileNotFoundError:
        pass


def set_random_word():
    """Returns the df index, sets a random word based on the df. If the df is empty, player won"""
    global df_index,df
    if df.empty:
        canvas.itemconfig(word, text="Congratulations! You win!", fill="black", font=("Ariel",30,"bold"))
    else:
        df_index = choice(df.index.values)
    return df_index


def get_random_words():
    global df_index,df
    return df.loc[df_index].array


def delete_word():
    delete_from_words_to_learn()
    delete_from_words_file()
    delete_from_df()

def right():
    global df
    """As the word is guessed, it is deleted from the files (words to learn and words), and from the current df. 
    If the df is empty, load into the df the words from the words file"""
    delete_word()
    if df.empty:
        df = pd.read_csv("data/words")
    flip()


def wrong():
    """If user is wrong, add the word to the words_to_learn file"""
    words = get_random_words()
    random_words_line = f"{words[0]},{words[1]}\n"
    word_already_present = False
    try:
        #Check if the word is already in the file
        with open("data/words_to_learn", "r") as file:
            for line in file.readlines():
                if line == random_words_line:
                    word_already_present = True
                    break
    except FileNotFoundError:
        with open("data/words_to_learn", "a") as file:
            file.write("italian,spanish\n")
            file.write(random_words_line)
    if not word_already_present:
        with open("data/words_to_learn", "a") as file:
            file.write(random_words_line)
    flip()


#-------------FLIP CARD----------------#


def start():
    start_button.destroy()
    flip()


def flip():
    global front
    if front:
        set_random_word()
        tick.config(state="disabled")
        cross.config(state="disabled")
        canvas.itemconfig(canvas_card, image=card_back_img)
        canvas.after(3000, flip)
    else:
        tick.config(state="active")
        cross.config(state="active")
        canvas.itemconfig(canvas_card, image=card_front_img)
    display_words()
    front = not front

#-------------RANDOM WORD----------------#


def display_words():
    words = get_random_words()
    if front:
        language = "italian"
        canvas.itemconfig(word_lang, text=language, fill="white")
        canvas.itemconfig(word, text=words[0], fill="white")
    else:
        language = "spanish"
        canvas.itemconfig(word_lang, text=language,fill="black")
        canvas.itemconfig(word, text=words[1],fill="black")

#-------------UI----------------#


window = Tk()
window.title("Flashy")
window.config(padx=50,pady=50, bg=BACKGROUND_COLOR)

card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_card = canvas.create_image(0, 0, image=card_front_img, anchor="nw")
word_lang = canvas.create_text(400, 150, font=("Ariel",40,"italic"))
word = canvas.create_text(400, 263, font=("Ariel",60,"italic"))
canvas.grid(row=0, columnspan=2, column=0, pady=(0,50))
start_button = Button(text="Start",padx=100,pady=100,font=("Ariel",60,"italic"),bg="white",command=start)
start_button.place(x=200, y=110)

# lang_text = Label(master=window,text="French",font=("Ariel",40,"italic"), bg="white")
# lang_text.place(x=300, y=150)
#
# word = Label(master=window,text="trouve",font=("Ariel",40,"bold"), bg="white")
# word.place(x=300, y=263)


tick_img = PhotoImage(file="./images/right.png")
tick = Button(image=tick_img, highlightthickness=0, command=right)
tick.grid(row=1, column=0)

cross_img = PhotoImage(file="./images/wrong.png")
cross = Button(image=cross_img, highlightthickness=0, command=wrong)
cross.grid(row=1, column=1)

#Disable buttons on start
tick.config(state="disabled")
cross.config(state="disabled")


start_words()

window.mainloop()
