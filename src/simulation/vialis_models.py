# import numpy as np
# from mesa import Agent, Model
# from mesa.space import MultiGrid
# from mesa.time import RandomActivation
# from mesa.visualization.modules.TextVisualization import TextElement
# from numpy.lib.function_base import angle

class Vehicle:
    def __init__(self, type, speed, pos):
        self.type = type
        self.speed = speed
        self.pos = pos


class biker:
    def __init__(self, speed, pos):
        self.speed = speed
        self.pos = pos


class trafficlight:
    def __init__(self, id):
        self.id = id


class Enviroment:
    def __init__(self):
        pass

