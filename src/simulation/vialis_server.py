"""
========== SERVER FILE ==========
This file contains the simulation (setup) of the MESA simulation.
The creation of the sliders can be found under the variables section!
=================================
"""

# For no gridline comment out L31 file
# mesa/visualization/templates/js/CanvasModule.js

# =============== IMPORTS =============== #
from vialis_models import Enviroment
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter


# ========== REGULAR FUNCTIONS ========== #
def person_portrayal(agent):

    colors = ["red", "blue", "green", "purple", "orange"]
    portrayal = {"Shape": "circle", "r": 5}

    if agent.type == 'voter':
        portrayal["Layer"] = 1
        if agent.voted_for == "grey":
            portrayal["Color"] = agent.voted_for
        else:
            portrayal["Color"] = colors[agent.voted_for]
            portrayal["Filled"] = "true"


    return portrayal


# ============== VARIABLES ============== #
grid = CanvasGrid(person_portrayal, 200, 200, 600, 600)
number_of_voters_slider = UserSettableParameter('slider', 'Voters', 200, 10, 600, 1)
number_of_candidates_slider = UserSettableParameter('slider', 'Candidates', 3, 1, 5, 1)
number_of_influencers_slider = UserSettableParameter('slider', 'Influencer', 3, 0, 5, 1)
number_of_steps_before_voting_slider = UserSettableParameter('slider', 'Number of stebs before voting', 10, 1, 30, 1)

# ============ SERVER SETUP ============= #
server = ModularServer(Enviroment, [grid], "Plurality Voting",
                        {
                            "V": number_of_voters_slider,
                            "C": number_of_candidates_slider,
                            "I": number_of_influencers_slider,
                            "S": number_of_steps_before_voting_slider,
                            "width": 200,
                            "height": 200
                        })
