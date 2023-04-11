import random

import requests.exceptions

from habit_tracker import HabitTracker,user_exists

habit_tracker = HabitTracker()

# habit_tracker.create_username("alfred")
# habit_tracker.save_user_in_file()


def start(user):
    # Create user / login
    if user_exists(user):
        print(habit_tracker.login(user))
    else:
        ok_signup = False
        while not ok_signup:
            try:
                print(habit_tracker.sign_up(user))
                ok_signup = True
            except requests.exceptions.HTTPError:
                start(input("Input another username"))  # Change accordingly if using a UI

    # HERE Already logged in
    # habit_tracker.load_graphs()
    # print(habit_tracker.graphs)
    graph_data = habit_tracker.create_graph(graph_name=f"Runner {random.randint(0,100)}", graph_units="kms", graph_type="float")
    print(graph_data)
    print(graph_data["response"].text)
    habit_tracker.add_pixel_today(graph_id=graph_data["graph_id"], qty=6)

    habit_tracker.save_graph_img(graph_data["graph_id"])


start("robertabc4")
