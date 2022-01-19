import numpy as np
from turtle import width
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
import random
# from mesa.visualization.modules.TextVisualization import TextElement
# from numpy.lib.function_base import angle


class agent(Agent):
    def __init__(self, unique_id: int, model: Model):
        super().__init__(unique_id, model)
        self.type = 'agent'


class traffic_light(Agent):
    def __init__(self, unique_id: int, model: Model):
        super().__init__(unique_id, model)
        self.type = 'tl'


class sensor(Agent):
    def __init__(self, unique_id: int, model: Model):
        super().__init__(unique_id, model)
        self.type = 'sensor'


class Enviroment(Model):
    def __init__(self, a, tl_nums, sen_nums, width, height) -> None:
        self.agent_nums = a
        self.tl_nums = tl_nums
        self.sen_nums = sen_nums
        self.tick = 0
        self.running = True
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.st_pos = [(0, 6), (0, 5), (0, 4), (7, 0), (8, 0), (14, 9), (14, 8), (14, 7)]
        self.tl_pos = [(5, 6), (5, 5), (5, 4), (9, 7), (9, 8), (9, 9), (7, 3), (8, 3)]
        self.sens_pos = [(4, 6), (4, 5), (4, 4), (10, 7), (10, 8), (10, 9), (7, 2), (8, 2)]

        for i in range(self.agent_nums):
            a = agent(i, self)
            self.schedule.add(a)
            start_cell = random.choice(self.st_pos)
            self.grid.place_agent(a, start_cell)

        for i in range(len(self.tl_pos)):
            a = traffic_light(i + self.agent_nums, self)
            self.schedule.add(a)
            self.grid.place_agent(a, self.tl_pos[i])

        for i in range(len(self.sens_pos)):
            a = sensor(i + self.agent_nums + len(self.tl_pos), self)
            self.schedule.add(a)
            self.grid.place_agent(a, self.sens_pos[i])
