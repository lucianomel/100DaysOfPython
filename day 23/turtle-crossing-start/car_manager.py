from turtle import Turtle
from random import choice
from random import randint

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10


class CarManager:
    def __init__(self):
        self.cars = []
        self.speed = STARTING_MOVE_DISTANCE
    def generate_car(self):
        new_car = Turtle("square")
        new_car.shapesize(stretch_wid=1, stretch_len=2)
        new_car.setheading(180)
        new_car.color(choice(COLORS))
        new_car.penup()
        new_car.goto(320, randint(-280, 260))
        self.cars.append(new_car)

    def move_cars(self):
        for car in self.cars:
            car.forward(self.speed)
            if car.xcor() < -320:
                self.cars.remove(car)

    def up_level(self):
        for car in self.cars:
            car.clear()
        self.speed += MOVE_INCREMENT
