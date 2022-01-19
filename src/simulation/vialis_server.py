"""
========== SERVER FILE ==========
This file contains the simulation (setup) of the MESA simulation.
The creation of the sliders can be found under the variables section!
=================================
"""

# For no gridline comment out L31 file
# mesa/visualization/templates/js/CanvasModule.js

# =============== IMPORTS =============== #
from turtle import width
from vialis_models import Enviroment
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter


# ========== REGULAR FUNCTIONS ========== #
def person_portrayal(agent):
    if agent.type == 'agent':
        portrayal = {"Shape": "arrowHead", "scale": 0.8, "Color": "blue", "Filled": "true", "Layer": 4}

        if agent.pos in [(0, 6), (0, 5), (0, 4)]:
            portrayal["heading_x"], portrayal["heading_y"] = 1, 0
        elif agent.pos in [(7, 0), (8, 0)]:
            portrayal["heading_x"], portrayal["heading_y"] = 0, 1
        elif agent.pos in [(14, 9), (14, 8), (14, 7)]:
            portrayal["heading_x"], portrayal["heading_y"] = -1, 0

    elif agent.type == 'tl':
        portrayal = {"Shape": "rect", "w": 0.75, "h": 0.75, "Color": "red", "Filled": "true", "Layer": 3}

    elif agent.type == 'sensor':
        portrayal = {"Shape": "circle", "r": 0.5, "Color": "black", "Layer": 2}

    return portrayal


g_width = 15
g_height = 11

# ============== VARIABLES ============== #
grid = CanvasGrid(person_portrayal, g_width, g_height, 600, 400)
number_of_agents_slider = UserSettableParameter('slider', 'Agents', 10, 1, 20, 1)
number_of_traffic_lights_slider = UserSettableParameter('slider', 'Traffic Lights', 4, 1, 8, 1)
number_of_sensors_slider = UserSettableParameter('slider', 'Sensors', 4, 1, 8, 1)

# ============ SERVER SETUP ============= #
server = ModularServer(Enviroment, [grid], "Traffic Simulation",
                        {
                            "a":        number_of_agents_slider,
                            "tl_nums":  number_of_traffic_lights_slider,
                            "sen_nums": number_of_sensors_slider,
                            "width":    g_width,
                            "height":   g_height
                        })

