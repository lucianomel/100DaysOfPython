from turtle import Turtle

FONT = ("Courier", 12, "normal")


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.level = 0
        self.init_scoreboard()

    def init_scoreboard(self):
        self.hideturtle()
        self.penup()
        self.goto(-200, 250)
        self.write_level()

    def write_level(self):
        self.clear()
        self.write(align="center", arg=f"Level: {self.level}", font=FONT)

    def increase_level(self):
        self.level += 1
        self.color("black")
        self.write_level()

    def game_over(self):
        self.goto(0, 0)
        self.write(align="center", arg="GAME OVER", font=FONT)
