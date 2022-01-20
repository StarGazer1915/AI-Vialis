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
from vialis_models import enviroment
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

# ========== REGULAR FUNCTIONS ========== #
def person_portrayal(agent):
    (x, y) = agent.pos
    (w, h) = agent.shape
    return {"Shape": "rect",
            "w": w,
            "h": h,
            "Layer": agent.layer,
            "Filled": "true",
            "x": x,
            "y": y,
            "Color": agent.color}

g_width = 56
g_height = 56
# ============== VARIABLES ============== #
grid = CanvasGrid(person_portrayal, g_width, g_height, g_width * 15, g_height * 15)
model_params = {"height": g_width,
                "width": g_height,
                "afs_sto_1_3_sen": UserSettableParameter("slider", "Afstand tussen stoplichten 1 t/m 3 en sensoren",
                                                                      value=7, min_value=1, max_value=14, step=1),
                "afs_sto_4_6_sen": UserSettableParameter("slider", "Afstand tussen stoplichten 4 t/m 6 en sensoren",
                                                                      value=12, min_value=1, max_value=23, step=1),
                "afs_sto_7_sen": UserSettableParameter("slider", "Afstand tussen stoplicht 7 en sensor",
                                                                      value=3, min_value=1, max_value=6, step=1),
                "afs_sto_8_11_sen": UserSettableParameter("slider", "Afstand tussen stoplichten 8 t/m 11 en sensoren",
                                                                      value=7, min_value=1, max_value=14, step=1),
                "afs_sto_12_14_sen": UserSettableParameter("slider", "Afstand tussen stoplichten 12 t/m 14 en sensoren",
                                                                      value=12, min_value=1, max_value=24, step=1),
                "afs_sto_15_16_sen": UserSettableParameter("slider", "Afstand tussen stoplichten 15 & 16 en sensoren",
                                                                      value=7, min_value=1, max_value=14, step=1)}

# ============ SERVER SETUP ============= #
server = ModularServer(enviroment, [grid], "Vialis", model_params)
