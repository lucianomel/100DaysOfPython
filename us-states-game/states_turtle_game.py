import turtle
import pandas as pd

# TODO: Make the text input appear in loop - OK
# TODO: Look for a country row in the csv, according to answear - OK
# TODO: Extract coordinates, make them a tuple and make a drawing turtle go to that position and write the state nameOK
# TODO: Keep track of number of guesses -OK
# TODO: Make game end when the user guesses wrong -OK


# game_data
def game_on(game_data):
    """game_data:{csv_path:...,image_path:...}"""
    screen = turtle.Screen()
    screen.title("Juego de las provincias")
    screen.setup(width=463, height=600)
    image = game_data["image_path"]
    screen.addshape(image)

    turtle.shape(image)

    # Import coordinates and states
    data = pd.read_csv(game_data["csv_path"])
    # Init loop variables
    game_is_on = True
    states_guessed = 0
    guessed_states = []
    n_provincias = data.state.size
    # Create writer
    tim = turtle.Turtle()
    tim.hideturtle()
    tim.penup()
    while game_is_on and states_guessed < n_provincias:
        answer_state = screen.textinput(title=f"{states_guessed}/{n_provincias}",
                                        prompt="Another province? (type with accents)").title()
        state_row = data[data.state == answer_state]
        # End if state was already guessed or if state is incorrect
        if state_row.empty or (answer_state in guessed_states):
            game_is_on = False
        else:
            # Retrieve state position
            state_position = (int(state_row["x"]), int(state_row["y"]))
            # Draw state name on image
            tim.goto(state_position)
            tim.write(answer_state)
            # Record guessed state
            guessed_states.append(answer_state)
            states_guessed += 1

    screen.bye()

    # look for missing states, sort one list + double index
    guessed_states.sort()
    missing_states = []
    j = 0
    states = data.state
    i = 0
    while i < states.size:
        state = states[i]
        if j < len(guessed_states) and state == guessed_states[j]:
            j += 1
        else:
            missing_states.append(state)
        i += 1

    return missing_states
