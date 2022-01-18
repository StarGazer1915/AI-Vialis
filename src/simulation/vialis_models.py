# import numpy as np
from mesa import Agent, Model
# from mesa.space import MultiGrid
# from mesa.time import RandomActivation
# from mesa.visualization.modules.TextVisualization import TextElement
# from numpy.lib.function_base import angle


class agent(Agent):
    def __init__(self, type, speed, direction, pos):
        self.type = type
        self.speed = speed
        self.direction = direction
        self.pos = pos


class traffic_light(Agent):
    def __init__(self, id):
        self.id = id


class sensor(Agent):
    def __init__(self, id):
        self.id = id


class enviroment(Model):
    def __init__(self):
        pass

