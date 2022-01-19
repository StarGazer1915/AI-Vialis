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
    portrayal = {
        "Shape": "arrowHead",
        "Filled": "true",
        "scale": 0.8,
        "heading_x": 1,
        "heading_y": 0
    }

    if agent.type == 'agent':
        portrayal["Color"] = "black"
        portrayal["Layer"] = 1
    elif agent.type == 'tl':
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1

    return portrayal

g_width = 15
g_height = 11

# ============== VARIABLES ============== #
grid = CanvasGrid(person_portrayal, g_width, g_height, 600, 400)
number_of_agents_slider = UserSettableParameter('slider', 'Agents', 10, 1, 20, 1)
number_of_traffic_lights_slider = UserSettableParameter('slider', 'Traffic Lights', 4, 1, 8, 1)

# ============ SERVER SETUP ============= #
server = ModularServer(Enviroment, [grid], "Traffic Simulation",
                        {
                            "a": number_of_agents_slider,
                            "tl_nums": number_of_traffic_lights_slider,
                            "width":    g_width,
                            "height":   g_height
                        })

