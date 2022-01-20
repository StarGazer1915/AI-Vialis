# import numpy as np
from turtle import width
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
# from mesa.visualization.modules.TextVisualization import TextElement
# from numpy.lib.function_base import angle

class agent(Agent):
    def __init__(self, pos, model):
        super().__init__(pos, model)
        #self.type = type
        #self.speed = speed
        #self.direction = direction
        self.pos = pos
        self.shape = (0.75, 0.75)
        self.layer = 2
        self.color = "blue"
        self.model = model

    def step(self):
        self.move()

    def move(self):
        """"Move the agent to a rand spot near him"""
        possible_poss = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        print(possible_poss)
        new_pos = self.random.choice(possible_poss)
        self.model.grid.move_agent(self, new_pos)

class road(Agent):
    def __init__(self, pos, shape):
        self.pos = pos
        self.layer = 0
        self.shape = shape
        self.color = "black"

class traffic_light(Agent):
    def __init__(self, unique_id, pos, shape):
        self.unique_id = unique_id
        self.pos = pos
        self.layer = 1
        self.shape = shape
        self.color = "red"

    def cycle(self):
        pass

class sensor(Agent):
    def __init__(self, unique_id, pos, shape):
        self.unique_id = unique_id
        self.pos = pos
        self.layer = 1
        self.shape = shape
        self.color = "gray"
    
    def detect(self):
        pass

class enviroment(Model):
    def __init__(self, width, height, afs_sto_1_3_sen, afs_sto_4_6_sen, afs_sto_7_sen, afs_sto_8_11_sen,
                 afs_sto_12_14_sen, afs_sto_15_16_sen):
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.running = True

        traffic_light_count = 0
        sensor_count = 0
        for (contents, x, y) in self.grid.coord_iter():
            # Horizontal road
            if (0 <= x <= 24 and y in [39, 38]) or (0 <= x <= 25 and y == 37) or (
                    30 <= x <= 55 and y in [16, 17, 18, 20]) or (29 <= x <= 55 and y == 19):
                self.grid._place_agent((x, y), road((x, y), (1, 0.5)))
            # Vertical road
            elif (x in [26, 29] and (0 <= y <= 15 or 21 <= y <= 36 or 40 <= y <= 55)) or (
                        x == 25 and 40 <= y <= 55) or (x == 27 and (21 <= y <= 36 or 40 <= y <= 55)) or (
                             x == 28 and (0 <= y <= 15 or 21 <= y <= 36)) or (
                             x == 30 and (29 <= y <= 36 or 40 <= y <= 55)):
                self.grid._place_agent((x, y), road((x, y), (0.5, 1)))

            # Traffic lights in horizontal road
            if (x == 24 and 37 <= y <= 39) or (x == 30 and 18 <= y <= 20):
                new_traffic_light = traffic_light(traffic_light_count, (x, y), (0.5, 0.75))
                self.grid._place_agent((x, y), new_traffic_light)
                self.schedule.add(new_traffic_light)
                traffic_light_count += 1
            # Traffic lights in vertical road
            elif (x in [28, 29] and y in [15, 36]) or ((x, y) == (30, 36)) or (x in [26, 27] and y in [21, 40]) or (
                        (x, y) == (25, 40)):
                new_traffic_light = traffic_light(traffic_light_count, (x, y), (0.75, 0.5))
                self.grid._place_agent((x, y), new_traffic_light)
                self.schedule.add(new_traffic_light)
                traffic_light_count += 1

            # Sensors in horizontal road
            if (x in [23, 23 - afs_sto_4_6_sen] and 37 <= y <= 39) or (
                    x in [31, 31 + afs_sto_12_14_sen] and 18 <= y <= 20):
                new_sensor = sensor(sensor_count, (x, y), (0.1, 0.3))
                self.grid._place_agent((x, y), new_sensor)
                sensor_count += 1
            # Sensors in vertical road
            elif (25 <= x <= 27 and y in [41, 41 + afs_sto_1_3_sen]) or (
                        x in [26, 27] and y in [22, 22 + afs_sto_8_11_sen]) or (
                             x in [28, 29] and y in [35, 35 - afs_sto_8_11_sen]) or (
                             x == 30 and y in [35, 35 - afs_sto_7_sen]) or (
                             x in [28, 29] and y in [14, 14 - afs_sto_15_16_sen]):
                new_sensor = sensor(sensor_count, (x, y), (0.3, 0.1))
                self.grid._place_agent((x, y), new_sensor)
                sensor_count += 1

            if (x, y) == (1, 39):
                new_agent = agent((x, y), self)
                self.grid._place_agent((x, y), new_agent)
                self.schedule.add(new_agent)

    def step(self):
        self.schedule.step()