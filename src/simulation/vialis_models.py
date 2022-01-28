from copy import copy
import numpy as np
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import BaseScheduler
import random as rn
from copy import deepcopy

class lcg:
    seed = 1
    a = 16
    c = 1
    m = 5000

    def lcg(self):
        self.seed = (self.a * self.seed + self.c) % self.m
        return self.seed / self.m

class vehicle(Agent):
    def __init__(self, unique_id, heading: tuple, color: str, path: list, min_ticks: int, start_ticks: int,
                 model: Model) -> None:
        super().__init__(unique_id, model)
        self.heading = heading
        self.color = color
        self.layer = 2
        self.path = path

        self.min_ticks = min_ticks
        self.start_ticks = start_ticks

    def remove(self) -> None:
        # 1 cell is 9 meter
        if self.color == "#FFFE00":
            self.model.avg_delays.append(self.model.tick - self.start_ticks - self.min_ticks)
        self.model.avg_speeds.append((self.min_ticks * 9 / (self.model.tick - self.start_ticks)) * 3.6)
        self.model.schedule.remove(self)
        self.model.grid.remove_agent(self)
        del self

    def new_pos_ang(self, angle: int):
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
            return possible_poss[6], (1, 0), True
        if 30 <= angle < 60:
            # North-east
            return possible_poss[7], (1, 1), False
        if 60 <= angle < 120:
            # North
            return possible_poss[4], (0, 1), True
        if 120 <= angle < 150:
            # North-west
            return possible_poss[2], (-1, 1), False
        if angle >= 150 or angle < -150:
            # West
            return possible_poss[1], (-1, 0), True
        if -150 <= angle < -120:
            # South-west
            return possible_poss[0], (-1, -1), False
        if -120 <= angle < -60:
            # South
            return possible_poss[3], (0, -1), True
        if -60 <= angle < -30:
            # South-east
            return possible_poss[5], (1, -1), False

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

        (new_pos, heading, change_heading) = self.new_pos_ang(angle)
        cell_list_contents = self.model.grid.get_cell_list_contents(new_pos)

        if not cell_list_contents:
            if change_heading:
                self.heading = heading
            self.model.grid.move_agent(self, new_pos)
        else:
            # Check if vehicle will be on another vehicle.
            if cell_list_contents[-1].color not in ["#FFFE00", "#5A9BFF"]:
                # Check if vehicle will be on red traffic light.
                if cell_list_contents[0].color != "red":
                    if change_heading:
                        self.heading = heading
                    self.model.grid.move_agent(self, new_pos)

                    # Check if vehicle will be on sensor.
                    if cell_list_contents[0].color == "gray":
                        sensor = cell_list_contents[0]
                        trafficlight = sensor.trafficlight

                        # Check if the sensor is the one which is farthest from the corresponding traffic light.
                        if sensor.unique_id[-1] == "2" and sensor.unique_id != "S8-2":
                            trafficlight.add_to_queue(self)
                        # Check if the sensor is the one which is closest from the corresponding traffic light.
                        elif sensor.unique_id[-1] == "1":
                            # Check if traffic light can be green.
                            if trafficlight.check_traffic_lights():
                                trafficlight.start_timer()
                elif cell_list_contents[0].color == "red":
                    trafficlight = cell_list_contents[0]
                    try:
                        # Try adding 1 to priority of the traffic lights corresponding to straight ahead.
                        self.model.traffic_lights[
                            int(self.model.straight[trafficlight.unique_id][2:]) - 1].priority += 1
                        trafficlight.priority += 1
                    except KeyError:
                        # Traffic light does not correspond to straight ahead, add 1 to priority
                        trafficlight.priority += 1

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
        "E1": [(29, 0), False, (0, 1)],
        "E2": [(28, 0), False, (0, 1)],
        "E3": [(0, 37), True, (1, 0)],
        "E4": [(0, 38), True, (1, 0)],
        "E5": [(25, 55), False, (0, -1)],
        "E6": [(26, 55), False, (0, -1)],
        "E7": [(27, 55), False, (0, -1)],
        "E8": [(55, 20), True, (-1, 0)],
        "E9": [(55, 19), True, (-1, 0)],
        "E10": [(55, 18), True, (-1, 0)]
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

    spawnpoint_ticks = {
        "E1": [43, 43],
        "E2": [68, 56, 56],
        "E3": [64, 77, 77],
        "E4": [47, 48],
        "E5": [42],
        "E6": [56, 69, 69],
        "E7": [56, 69, 69],
        "E8": [74, 62, 62],
        "E9": [76, 64, 64],
        "E10": [48]
    }

    def __init__(self, unique_id: str, color: str, model: Model) -> None:
        super().__init__(unique_id, model)
        self.name = unique_id
        self.shape = (1, .75) if self.spawnpoints_cords[self.name][1] else (.75, 1)
        self.color = color
        self.layer = 0
        self.pos = self.spawnpoints_cords[self.name][0]
        self.paths = self.spawnpoint_paths[self.name]

    def spawn_vehicle(self) -> None:
        path = rn.choice(self.paths)
        min_ticks = self.spawnpoint_ticks[self.unique_id][self.paths.index(path)]

        new_vehicle = vehicle(self.model.vehicle_counter, self.spawnpoints_cords[self.name][2],
                              "#FFFE00" if self.name == "E8" else "#5A9BFF", copy(path), min_ticks, self.model.tick,
                              self.model)
        self.model.grid.place_agent(new_vehicle, self.pos)
        self.model.schedule.add(new_vehicle)
        self.model.vehicle_counter += 1
        return new_vehicle

    lcg = lcg()

    def step(self) -> None:
        if self.model.tick % 2 == 0:
            if self.lcg.lcg() < .15:
                self.spawn_vehicle()

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

    traffic_light_configs = {
        # Traffic lights in list have to be red in order for the corresponding traffic light to be green.
        # Traffic lights in list can be green when the corresponding traffic light is green.
        # Cooldown
        "C-TL1": (["TL4"], [], 2),
        "C-TL2": (["TL4", "TL6", "TL7"], ["TL1", "TL3"], 6),
        "C-TL3": (["TL7"], [], 6),
        "C-TL4": (["TL1", "TL2", "TL7"], ["TL6"], 8),
        "C-TL5": ([], [], 2),
        "C-TL6": (["TL2"], [], 4),
        "C-TL7": (["TL2", "TL3", "TL4"], ["TL1", "TL6"], 7),
        "C-TL8": (["TL12"], ["TL9"], 4),
        "C-TL9": (["TL12"], ["TL8"], 4),
        "C-TL10": (["TL12", "TL13", "TL14", "TL15"], ["TL8", "TL9", "TL11"], 7),
        "C-TL11": (["TL14", "TL15"], [], 5),
        "C-TL12": (["TL8", "TL9", "TL10", "TL14", "TL15"], ["TL13"], 8),
        "C-TL13": (["TL10"], [], 2),
        "C-TL14": (["TL10", "TL11", "TL12"], ["TL8", "TL9", "TL15"], 4),
        "C-TL15": (["TL10", "TL11", "TL12"], ["TL8", "TL9", "TL14"], 4)
    }

    def __init__(self, unique_id: str, model: Model) -> None:
        super().__init__(unique_id, model)
        self.name = unique_id
        self.shape = (.75, .5) if self.traffic_lights_details[self.name][1] else (.5, .75)
        self.color = "red"
        self.layer = 1
        self.pos = self.traffic_lights_details[self.name][0]

        self.vehicle_queue = []
        self.timer = 0
        self.cooldown = 0
        self.priority = 0

    def calc_queue_prio(self) -> int:
        temp_priority = deepcopy(self.priority)
        for vehicle in self.vehicle_queue:
            temp_priority += 4 if vehicle.color == "#FFFE00" else 1
        return temp_priority

    def check_traffic_lights(self) -> bool:
        # Check if traffic lights in config are red, have a cooldown or have a longer queue.
        for config in self.traffic_light_configs[f"C-{self.name}"][0]:
            trafficlight = self.model.traffic_lights[int(config[2:]) - 1]
            #print(f"Traffic light {trafficlight.unique_id}:\n   Priority {trafficlight.priority} ({trafficlight.calc_queue_prio()})")
            if trafficlight.color != "red" or trafficlight.cooldown > 0 or \
                    self.calc_queue_prio() < trafficlight.calc_queue_prio():
                    return False
        return True

    def add_to_queue(self, vehicle: Agent) -> None:
        try:
            # Try adding the vehicle id to vehicle queue of the traffic lights corresponding to straight ahead.
            self.model.traffic_lights[int(self.model.straight[self.unique_id][2:]) - 1].vehicle_queue.append(vehicle)
            self.vehicle_queue.append(vehicle)
        except KeyError:
            # Traffic light does not correspond to straight ahead, add vehicle id to vehicle queue.
            self.vehicle_queue.append(vehicle)

    def remove_from_queue(self, vehicle: Agent) -> None:
        try:
            # Try removing the vehicle from vehicle queue of the traffic lights corresponding to straight ahead.
            self.model.traffic_lights[int(self.model.straight[self.unique_id][2:]) - 1].vehicle_queue.remove(vehicle)
            self.vehicle_queue.remove(vehicle)
        except KeyError:
            # Traffic light does not correspond to straight ahead, remove vehicle from vehicle queue.
            self.vehicle_queue.remove(vehicle)

    def start_timer(self) -> None:
        try:
            # Try starting the timer of the traffic lights corresponding to straight ahead.
            simultaneous_traffic_light = self.model.traffic_lights[int(self.model.straight[self.unique_id][2:]) - 1]
            # Timer = amount of vehicles in queue + 2.
            simultaneous_traffic_light.timer = len(simultaneous_traffic_light.vehicle_queue) + 2
            self.timer = len(self.vehicle_queue) + 2
        except KeyError:
            # Traffic light does not correspond to straight ahead, start timer.
            self.timer = len(self.vehicle_queue) + 2

    def cycle(self) -> str:
        if self.timer == 1:
            return "#FF9021"  # Orange
        elif self.timer >= 2:
            return "#33BD00"  # Green
        else:
            return "red"

    def step(self) -> None:
        self.color = self.cycle()

        if self.cooldown > 0:
            self.cooldown -= 1
        elif self.cooldown == 0:
            if self.timer > 1:
                self.priority = 0
                self.timer -= 1
            elif self.timer == 1:
                self.timer -= 1
                self.cooldown = self.traffic_light_configs[f"C-{self.name}"][2]

class sensor(Agent):
    def __init__(self, unique_id: str, flip: bool, trafficlight: Agent, model: Model) -> None:
        super().__init__(unique_id, model)
        self.name = unique_id
        self.shape = (.3, .1) if flip else (.1, .3)
        self.color = "gray"
        self.layer = 1

        self.trafficlight = trafficlight

    def detect(self) -> None:
        cell_list_contents = self.model.grid.get_cell_list_contents(self.pos)
        # Check if vehicle is on sensor that is closest to the corresponding traffic light.
        if self.name[-1] == "1" and cell_list_contents[-1].color in ["#FFFE00", "#5A9BFF"]:
            vehicle = cell_list_contents[-1]

            # Check if traffic light is not red and vehicle id is in the vehicle queue
            # of the corresponding traffic light.
            if self.trafficlight.color != "red" and vehicle in self.trafficlight.vehicle_queue:
                self.trafficlight.remove_from_queue(vehicle)
            # Check if traffic light can be green.
            if self.trafficlight.check_traffic_lights():
                self.trafficlight.start_timer()

    def step(self) -> None:
        self.detect()

class environment(Model):
    def __init__(self, width, height, afs_sto_1_2_sen, afs_sto_3_4_sen, afs_sto_5_7_sen, afs_sto_8_sen,
                 afs_sto_9_10_sen, afs_sto_11_12_sen, afs_sto_13_15_sen, spawnpoint_color, deathzone_color) -> None:
        self.grid = MultiGrid(width, height, False)
        self.schedule = BaseScheduler(self)
        self.running = True
        self.tick = 0
        self.vehicle_counter = 0
        self.traffic_lights = []
        self.avg_speeds = []
        self.avg_delays = []

        self.spawnpoint_color = spawnpoint_color
        self.deathzone_color = deathzone_color

        self.sensors_details = {
            "S1-1": [(29, 14), True],
            "S1-2": [(29, 14 - afs_sto_1_2_sen), True, afs_sto_1_2_sen],
            "S2-1": [(28, 14), True],
            "S2-2": [(28, 14 - afs_sto_1_2_sen), True, afs_sto_1_2_sen],
            "S3-1": [(26, 22), True],
            "S3-2": [(26, 22 + afs_sto_3_4_sen), True, afs_sto_3_4_sen],
            "S4-1": [(27, 22), True],
            "S4-2": [(27, 22 + afs_sto_3_4_sen), True, afs_sto_3_4_sen],
            "S5-1": [(31, 20), False],
            "S5-2": [(31 + afs_sto_5_7_sen, 20), False, afs_sto_5_7_sen],
            "S6-1": [(31, 19), False],
            "S6-2": [(31 + afs_sto_5_7_sen, 19), False, afs_sto_5_7_sen],
            "S7-1": [(31, 18), False],
            "S7-2": [(31 + afs_sto_5_7_sen, 18), False, afs_sto_5_7_sen],
            "S8-1": [(30, 35), True],
            "S8-2": [(30, 35 - afs_sto_8_sen), True, afs_sto_8_sen],
            "S9-1": [(29, 35), True],
            "S9-2": [(29, 35 - afs_sto_9_10_sen), True, afs_sto_9_10_sen],
            "S10-1": [(28, 35), True],
            "S10-2": [(28, 35 - afs_sto_9_10_sen), True, afs_sto_9_10_sen],
            "S11-1": [(23, 37), False],
            "S11-2": [(23 - afs_sto_11_12_sen, 37), False, afs_sto_11_12_sen],
            "S12-1": [(23, 38), False],
            "S12-2": [(23 - afs_sto_11_12_sen, 38), False, afs_sto_11_12_sen],
            "S13-1": [(25, 41), True],
            "S13-2": [(25, 41 + afs_sto_13_15_sen), True, afs_sto_13_15_sen],
            "S14-1": [(26, 41), True],
            "S14-2": [(26, 41 + afs_sto_13_15_sen), True, afs_sto_13_15_sen],
            "S15-1": [(27, 41), True],
            "S15-2": [(27, 41 + afs_sto_13_15_sen), True, afs_sto_13_15_sen]
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

        self.straight = {"TL8": "TL9",
                         "TL9": "TL8",
                         "TL14": "TL15",
                         "TL15": "TL14"}

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
            self.traffic_lights.append(new_traffic_light)
            self.grid.place_agent(new_traffic_light, new_traffic_light.pos)
            self.schedule.add(new_traffic_light)

    def gen_sensors(self) -> None:
        for x in range(1, 16):
            for sensor_code in range(1, 3):
                new_sensor = sensor(f"S{x}-{sensor_code}", self.sensors_details[f"S{x}-{sensor_code}"][1],
                                    self.traffic_lights[x - 1], self)
                self.grid.place_agent(new_sensor, self.sensors_details[new_sensor.name][0])
                self.schedule.add(new_sensor)

    def step(self) -> None:
        self.tick += 1
        self.schedule.step()
        if self.tick % 1200 == 0:
            print(f"Average speed is {round(sum(self.avg_speeds) / len(self.avg_speeds), 2)} km/h")
            print(f"Average bus delay is {round(sum(self.avg_delays) / len(self.avg_delays), 2)} seconds")