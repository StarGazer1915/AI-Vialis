# import numpy as np
from turtle import width
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
# from mesa.visualization.modules.TextVisualization import TextElement
# from numpy.lib.function_base import angle


class agent(Agent):
    def __init__(self, unique_id: int, model: Model):
        super().__init__(unique_id, model)
        self.type = 'agent'

    def move(self):
        pass


class traffic_light(Agent):
    def __init__(self, unique_id: int, model: Model):
        super().__init__(unique_id, model)
        self.type = 'tl'

    def cycle(self):
        pass


class sensor(Agent):
    def __init__(self, id):
        self.id = id
    
    def detect(self):
        pass


class Enviroment(Model):
    def __init__(self, a, tl_nums, width, height) -> None:
        self.agent_nums = a
        self.tl_nums = tl_nums
        self.tick = 0
        self.running = True
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)

        for i in range(self.agent_nums):
            a = agent(i, self)
            self.schedule.add(a)
            start_cell = (0, 7)
            self.grid.place_agent(a, start_cell)

        for i in range(self.tl_nums):
            a = traffic_light(i + self.agent_nums, self)
            self.schedule.add(a)
            start_cell = (14, 7)
            self.grid.place_agent(a, start_cell)
