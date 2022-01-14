from vialis.classes.model import Vialis
from vialis.portrayal import vialis_portrayal, COLORS

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

canvas_element = CanvasGrid(vialis_portrayal, 100, 100, 500, 500)

model_params = {
    "height": 100,
    "width": 100,
}

server = ModularServer(Vialis, [canvas_element], "Vialis", model_params)