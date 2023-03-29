import random
import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

tim = Player()
car_manager = CarManager()
scoreboard = Scoreboard()

screen.onkey(tim.move, "Up")
screen.listen()

game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()
    car_manager.move_cars()
    if random.randint(1, 5) == 1:
        car_manager.generate_car()
    if tim.reached_finish_line():
        car_manager.up_level()
        scoreboard.increase_level()
        tim.back_to_start()
    if tim.collides(car_manager):
        scoreboard.game_over()
        game_is_on = False

screen.exitonclick()
# TODO: Create a turtle and make it move forwards with the up key - OK
# TODO: Create a car at a random position with a random color and make it move from right to left - OK
# TODO: Randomly create (or not, 1/5) a car every 0.1 seconds - OK
# TODO: Remove cars out of screen (when turtle reached finish line) and from the car manager (when cars reach right)
#  - OK
# TODO: Create a scoreboard that says level at the top left of the screen. Create a function to increase score - OK
# TODO: When the turtle arrives to the top, move it back to the bottom and increase score. Make the car speed increase
#  - OK
# TODO: If the turtle collides with a car, print game over and stop the game