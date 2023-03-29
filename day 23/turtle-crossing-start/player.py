from turtle import Turtle

STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280


class Player(Turtle):
    def __init__(self):
        super().__init__("turtle")
        self.create_turtle()

    def create_turtle(self):
        self.penup()
        self.setheading(90)
        self.goto(STARTING_POSITION)

    def move(self):
        self.forward(MOVE_DISTANCE)

    def reached_finish_line(self):
        return self.ycor() >= FINISH_LINE_Y

    def back_to_start(self):
        self.goto(STARTING_POSITION)

    def collides(self, car_manager):
        for car in car_manager.cars:
            if abs(self.xcor() - car.xcor()) < 20 and abs(self.ycor() - car.ycor()) < 15:
                return True
        return False
