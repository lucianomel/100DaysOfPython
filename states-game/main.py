from end_gui import show_missing_states
from states_turtle_game import game_on

GAME_CSV_PATH = "argentina_coords.csv"
GAME_IMAGE_PATH = "arg_map.gif"
GAME_DATA = {"csv_path": GAME_CSV_PATH, "image_path": GAME_IMAGE_PATH}

missing_states = game_on(GAME_DATA)

show_missing_states(missing_states)
