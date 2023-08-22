from turtle import Turtle
import random
COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10


class CarManager:
    def __init__(self):
        self.all_cars = []
        self.cars_speed = STARTING_MOVE_DISTANCE
    def create_cars(self):
        random_chance = random.randint(1, 6)
        if random_chance == 1:
            cars = Turtle(shape="square")
            cars.shapesize(stretch_wid=1, stretch_len=2)
            cars.penup()
            cars.color(random.choice(COLORS))
            position_y = random.randint(-250, 250)
            cars.goto(300, position_y)
            self.all_cars.append(cars)
    def move_cars(self):
        for car in self.all_cars:
            car.backward(self.cars_speed)
    def level_up(self):
        self.cars_speed += MOVE_INCREMENT