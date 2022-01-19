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

    portrayal = {"Shape": "circle", "r": 5}


    return portrayal

g_width = 100
g_height = 100
# ============== VARIABLES ============== #
grid = CanvasGrid(person_portrayal, g_width, g_height, 600, 600)

# ============ SERVER SETUP ============= #
server = ModularServer(enviroment, [grid], "Plurality Voting",
                        {
                            "width":    g_width,
                            "height":   g_height
                        })
