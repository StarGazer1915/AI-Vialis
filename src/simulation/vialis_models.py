# import numpy as np
from turtle import width
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
# from mesa.visualization.modules.TextVisualization import TextElement
# from numpy.lib.function_base import angle


class agent(Agent):
    def __init__(self, type, speed, direction, pos):
        self.type = type
        self.speed = speed
        self.direction = direction
        self.pos = pos

    def move():
        pass

class traffic_light(Agent):
    def __init__(self, id):
        self.id = id

    def cycle():
        pass


class sensor(Agent):
    def __init__(self, id):
        self.id = id
    
    def detect():
        pass


class enviroment(Model):
    def __init__(self, width, height):
        self.grid = MultiGrid(width, height, False)

    def step():
        pass
