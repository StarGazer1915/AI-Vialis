from copy import copy
import numpy as np
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import BaseScheduler
import random as rn

class car(Agent):
    def __init__(self, unique_id, path: list, model: Model) -> None:
        super().__init__(unique_id, model)
        self.shape = (.75, .75)
        self.color = "#5A9BFF"
        self.layer = 2
        self.path = path

    def remove(self) -> None:
        self.model.schedule.remove(self)
        self.model.grid.remove_agent(self)
        del self

    def new_pos_ang(self, angle: int) -> tuple:
        """Get a new position for the agent near him, based on an angle"""
        # Set all coordinates around the agent
        (x, y) = self.pos
        possible_poss = (
            (x - 1, y - 1),
            (x - 1, y),
            (x - 1, y + 1),
            (x, y - 1),
            (x, y + 1),
            (x + 1, y - 1),
            (x + 1, y),
            (x + 1, y + 1)
        )

        if -30 <= angle < 30:
            # East
            return possible_poss[6]
        if 30 <= angle < 60:
            # North-east
            return possible_poss[7]
        if 60 <= angle < 120:
            # North
            return possible_poss[4]
        if 120 <= angle < 150:
            # North-west
            return possible_poss[2]
        if angle >= 150 or angle < -150:
            # West
            return possible_poss[1]
        if -150 <= angle < -120:
            # South-west
            return possible_poss[0]
        if -120 <= angle < -60:
            # South
            return possible_poss[3]
        if -60 <= angle < -30:
            # South-east
            return possible_poss[5]

    def get_angle(self, cord) -> int:
        """Get the angle of the next point relative to the agents position """
        x1 = (cord[1] - self.pos[1])
        x2 = (cord[0] - self.pos[0])

        angle = np.arctan2(x1, x2) * 180 / np.pi
        return angle

    def move(self) -> None:
        # If a checkpoint has been reached then delete it from the route.
        if self.path[0] == self.pos:
            del self.path[0]

        # Calculate which direction to move next and move there.
        angle = self.get_angle(self.path[0])
        try:
            new_pos = self.new_pos_ang(angle)
            cell_list_contents = self.model.grid.get_cell_list_contents(new_pos)

            if not cell_list_contents:
                self.model.grid.move_agent(self, new_pos)
            else:
                # Check if car will be on another car.
                if cell_list_contents[-1].color == "#5A9BFF":
                    print(f"Tried to move Car {self.unique_id} on Car {cell_list_contents[-1].unique_id}")
                else:
                    # Check if car will be on red traffic light.
                    if cell_list_contents[0].color != "red":
                        self.model.grid.move_agent(self, new_pos)

                        # Check if car will be on sensor.
                        if cell_list_contents[0].color == "gray":
                            sensor = cell_list_contents[0].unique_id
                            print(f"Sensor {sensor} detected Car {self.unique_id}")
        except KeyError:
            print(f"Tried to move Car {self.unique_id} out of bounds")

    def step(self) -> None:
        # Kill itself if it hase reached the end of the route
        cell_list_contents = self.model.grid.get_cell_list_contents(self.pos)
        try:
            if cell_list_contents[0].death:
                self.remove()
        except AttributeError:
            self.move()

class spawnpoint(Agent):
    spawnpoints_cords = {
        "E1": [(29, 0), False],
        "E2": [(28, 0), False],
        "E3": [(0, 37), True],
        "E4": [(0, 38), True],
        "E5": [(25, 55), False],
        "E6": [(26, 55), False],
        "E7": [(27, 55), False],
        "E8": [(55, 20), True],
        "E9": [(55, 19), True],
        "E10": [(55, 18), True]
    }

    spawnpoint_paths = {
        "E1": [[(29, 16), (55, 16)],  # To deathzone 6
               [(29, 16), (36, 17), (55, 17)]],  # To deathzone 5
        "E2": [[(28, 39), (0, 39)],  # To deathzone 2
               [(29, 22), (29, 55)],  # To deathzone 3
               [(29, 22), (30, 28), (30, 55)]],  # To deathzone 4
        "E3": [[(26, 37), (26, 0)],  # To deathzone 1
               [(27, 37), (27, 16), (55, 16)],  # To deathzone 6
               [(27, 37), (27, 16), (36, 17), (55, 17)]],  # To deathzone 5
        "E4": [[(29, 38), (29, 55)],  # To deathzone 3
               [(30, 38), (30, 55)]],  # To deathzone 4
        "E5": [[(25, 39), (0, 39)]],  # To deathzone 2
        "E6": [[(26, 0)],  # To deathzone 1
               [(27, 35), (27, 16), (55, 16)],  # To deathzone 6
               [(27, 35), (27, 16), (36, 17), (55, 17)]],  # To deathzone 5
        "E7": [[(26, 35), (26, 0)],  # To deathzone 1
               [(27, 16), (55, 16)],  # To deathzone 6
               [(27, 16), (36, 17), (55, 17)]],  # To deathzone 5
        "E8": [[(29, 20), (28, 22), (28, 39), (0, 39)],  # To deathzone 2
               [(29, 20), (29, 55)],  # To deathzone 3
               [(29, 20), (30, 28), (30, 55)]],  # To deathzone 4
        "E9": [[(28, 19), (28, 39), (0, 39)],  # To deathzone 2
               [(28, 19), (29, 22), (29, 55)],  # To deathzone 3
               [(28, 19), (29, 22), (30, 28), (30, 55)]],  # To deathzone 4
        "E10": [[(26, 18), (26, 0)]]  # To deathzone 1
    }

    def __init__(self, unique_id: str, color: str, model: Model) -> None:
        super().__init__(unique_id, model)
        self.name = unique_id
        self.shape = (1, .75) if self.spawnpoints_cords[self.name][1] else (.75, 1)
        self.color = color
        self.layer = 0
        self.pos = self.spawnpoints_cords[self.name][0]
        self.paths = self.spawnpoint_paths[self.name]

    def spawn_car(self) -> None:
        path = rn.choice(self.paths)

        new_car = car(self.model.car_counter, copy(path), self.model)
        self.model.grid.place_agent(new_car, self.pos)
        self.model.schedule.add(new_car)

    def step(self) -> None:
        if self.model.tick % 2 == 0:
            if rn.random() > .5:
                self.spawn_car()
                self.model.car_counter += 1

class road(Agent):
    def __init__(self, flip: bool) -> None:
        self.portrayal_type = "rect"
        self.shape = (1, .75) if flip else (.75, 1)
        self.color = "black"
        self.layer = 0

class deathzone(Agent):
    deathzone_cords = {
        "D1": [(26, 0), False],
        "D2": [(0, 39), True],
        "D3": [(29, 55), False],
        "D4": [(30, 55), False],
        "D5": [(55, 17), True],
        "D6": [(55, 16), True],
    }

    def __init__(self, unique_id: str, color: str, model: Model) -> None:
        super().__init__(unique_id, model)
        self.name = unique_id
        self.portrayal_type = "rect"
        self.shape = (1, .75) if self.deathzone_cords[self.name][1] else (.75, 1)
        self.color = color
        self.layer = 0
        self.pos = self.deathzone_cords[self.name][0]
        self.death = True

class traffic_light(Agent):
    traffic_lights_details = {
        "TL1": [(29, 15), True],
        "TL2": [(28, 15), True],
        "TL3": [(26, 21), True],
        "TL4": [(27, 21), True],
        "TL5": [(30, 20), False],
        "TL6": [(30, 19), False],
        "TL7": [(30, 18), False],
        "TL8": [(30, 36), True],
        "TL9": [(29, 36), True],
        "TL10": [(28, 36), True],
        "TL11": [(24, 37), False],
        "TL12": [(24, 38), False],
        "TL13": [(25, 40), True],
        "TL14": [(26, 40), True],
        "TL15": [(27, 40), True],
    }

    def __init__(self, unique_id: str, model: Model) -> None:
        super().__init__(unique_id, model)
        self.name = unique_id
        self.shape = (.75, .5) if self.traffic_lights_details[self.name][1] else (.5, .75)
        self.color = "#33BD00"
        self.layer = 1
        self.pos = self.traffic_lights_details[self.name][0]

    def cycle(self) -> None:
        # red = "red"
        # orange = "#FF9021"
        # green = "#33BD00"
        pass

class sensor(Agent):
    def __init__(self, unique_id: str, flip: bool, model: Model) -> None:
        super().__init__(unique_id, model)
        self.name = unique_id
        self.shape = (.3, .1) if flip else (.1, .3)
        self.color = "gray"
        self.layer = 1

class enviroment(Model):
    def __init__(self, width, height, afs_sto_1_2_sen, afs_sto_3_4_sen, afs_sto_5_7_sen, afs_sto_8_sen,
                 afs_sto_9_10_sen, afs_sto_11_12_sen, afs_sto_13_15_sen, spawnpoint_color, deathzone_color) -> None:
        self.grid = MultiGrid(width, height, False)
        self.schedule = BaseScheduler(self)
        self.running = True
        self.tick = 0
        self.car_counter = 0

        self.spawnpoint_color = spawnpoint_color
        self.deathzone_color = deathzone_color

        self.sensors_details = {
            "S1-1": [(29, 14), True],
            "S1-2": [(29, 14 - afs_sto_1_2_sen), True],
            "S2-1": [(28, 14), True],
            "S2-2": [(28, 14 - afs_sto_1_2_sen), True],
            "S3-1": [(26, 22), True],
            "S3-2": [(26, 22 + afs_sto_3_4_sen), True],
            "S4-1": [(27, 22), True],
            "S4-2": [(27, 22 + afs_sto_3_4_sen), True],
            "S5-1": [(31, 20), False],
            "S5-2": [(31 + afs_sto_5_7_sen, 20), False],
            "S6-1": [(31, 19), False],
            "S6-2": [(31 + afs_sto_5_7_sen, 19), False],
            "S7-1": [(31, 18), False],
            "S7-2": [(31 + afs_sto_5_7_sen, 18), False],
            "S8-1": [(30, 35), True],
            "S8-2": [(30, 35 - afs_sto_8_sen), True],
            "S9-1": [(29, 35), True],
            "S9-2": [(29, 35 - afs_sto_9_10_sen), True],
            "S10-1": [(28, 35), True],
            "S10-2": [(28, 35 - afs_sto_9_10_sen), True],
            "S11-1": [(23, 37), False],
            "S11-2": [(23 - afs_sto_11_12_sen, 37), False],
            "S12-1": [(23, 38), False],
            "S12-2": [(23 - afs_sto_11_12_sen, 38), False],
            "S13-1": [(25, 41), True],
            "S13-2": [(25, 41 + afs_sto_13_15_sen), True],
            "S14-1": [(26, 41), True],
            "S14-2": [(26, 41 + afs_sto_13_15_sen), True],
            "S15-1": [(27, 41), True],
            "S15-2": [(27, 41 + afs_sto_13_15_sen), True]
        }

        self.roadzones = {
            "R1": [(26, 1), (26, 15), False],
            "R2": [(28, 1), (29, 15), False],
            "R3": [(30, 16), (54, 16), True],
            "R4": [(36, 17), (54, 17), True],
            "R5": [(30, 18), (54, 20), True],
            "R6": [(26, 21), (29, 36), False],
            "R7": [(30, 28), (30, 36), False],
            "R8": [(1, 37), (24, 39), True],
            "R9": [(25, 40), (27, 54), False],
            "R10": [(29, 40), (30, 54), False]
        }

        self.gen_spawnpoints()
        self.gen_deathzones()
        self.gen_traffic_lights()
        self.gen_sensors()
        self.gen_road()

    def gen_spawnpoints(self) -> None:
        for spawnpoint_code in range(1, 11):
            new_spawnpoint = spawnpoint(f"E{spawnpoint_code}", self.spawnpoint_color, self)
            self.grid.place_agent(new_spawnpoint, new_spawnpoint.pos)
            self.schedule.add(new_spawnpoint)

    def gen_deathzones(self) -> None:
        for deathzone_code in range(1, 7):
            new_deathzone = deathzone(f"D{deathzone_code}", self.deathzone_color, self)
            self.grid.place_agent(new_deathzone, new_deathzone.pos)
            self.schedule.add(new_deathzone)

    def gen_road(self) -> None:
        for roadzone in self.roadzones:
            cord1, cord2, flip = self.roadzones[roadzone]
            for x_cord in range(cord1[0], cord2[0] + 1):
                for y_cord in range(cord1[1], cord2[1] + 1):
                    new_road = road(flip)
                    self.grid.place_agent(new_road, (x_cord, y_cord))

    def gen_traffic_lights(self) -> None:
        for traffic_light_code in range(1, 16):
            new_traffic_light = traffic_light(f"TL{traffic_light_code}", self)
            self.grid.place_agent(new_traffic_light, new_traffic_light.pos)
            self.schedule.add(new_traffic_light)

    def gen_sensors(self) -> None:
        for sensor_code1 in range(1, 16):
            for sensor_code2 in range(1, 3):
                new_sensor = sensor(f"S{sensor_code1}-{sensor_code2}",
                                    self.sensors_details[f"S{sensor_code1}-{sensor_code2}"][1], self)
                self.grid.place_agent(new_sensor, self.sensors_details[new_sensor.name][0])
                self.schedule.add(new_sensor)

    def step(self) -> None:
        self.tick += 1
        self.schedule.step()
