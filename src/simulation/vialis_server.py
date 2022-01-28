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
from vialis_models import environment
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

# ========== REGULAR FUNCTIONS ========== #
def person_portrayal(agent):
    (x, y) = agent.pos

    try:
        (w, h) = agent.shape

        portrayal = {"Shape": "rect",
                     "w": w,
                     "h": h,
                     "Color": agent.color,
                     "Filled": "true",
                     "Layer": agent.layer,
                     "x": x,
                     "y": y}
    except AttributeError:
        (heading_x, heading_y) = agent.heading

        portrayal = {"Shape": "arrowHead",
                     "scale": .75,
                     "heading_x": heading_x,
                     "heading_y": heading_y,
                     "Color": agent.color,
                     "Filled": "true",
                     "Layer": agent.layer,
                     "x": x,
                     "y": y}

    return portrayal

g_width = 56
g_height = 56
# ============== VARIABLES ============== #
grid = CanvasGrid(person_portrayal, g_width, g_height, g_width * 15, g_height * 15)
model_params = {"height": g_width,
                "width": g_height,
                "afs_sto_1_2_sen": UserSettableParameter("slider", "Afstand tussen stoplichten 1 & 2 en sensoren",
                                                         value=13, min_value=1, max_value=13, step=1),
                "afs_sto_3_4_sen": UserSettableParameter("slider", "Afstand tussen stoplichten 3 & 4 en sensoren",
                                                         value=13, min_value=1, max_value=13, step=1),
                "afs_sto_5_7_sen": UserSettableParameter("slider", "Afstand tussen stoplichten 5 t/m 7 en sensoren",
                                                         value=12, min_value=1, max_value=23, step=1),
                "afs_sto_8_sen": UserSettableParameter("slider", "Afstand tussen stoplicht 8 en sensor",
                                                       value=7, min_value=1, max_value=7, step=1),
                "afs_sto_9_10_sen": UserSettableParameter("slider", "Afstand tussen stoplichten 9 & 10 en sensoren",
                                                          value=13, min_value=1, max_value=13, step=1),
                "afs_sto_11_12_sen": UserSettableParameter("slider", "Afstand tussen stoplichten 11 & 12 en sensoren",
                                                           value=11, min_value=1, max_value=22, step=1),
                "afs_sto_13_15_sen": UserSettableParameter("slider", "Afstand tussen stoplichten 13 t/m 15 en sensoren",
                                                           value=13, min_value=1, max_value=13, step=1),
                "car_spawnrate": UserSettableParameter("slider", "Car spawnrate in %", value=14, min_value=4,
                                                       max_value=24, step=1),
                "bus_spawnrate": UserSettableParameter("slider", "Bus spawnrate in minutes", value=6, min_value=1,
                                                       max_value=11, step=1),
                "spawnpoint_color": UserSettableParameter("choice", "Spawnpoint color", value="black",
                                                          choices=["black", "#FFEC00"]),
                "deathzone_color": UserSettableParameter("choice", "Deathzone color", value="black",
                                                         choices=["black", "#FF5A5A"])}

# ============ SERVER SETUP ============= #
server = ModularServer(environment, [grid], "Vialis", model_params)