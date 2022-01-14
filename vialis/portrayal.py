COLORS = {"None": "#DDDDDD", "Car": "#FFA100", "Bus": "#006FFF"}

def vialis_portrayal(agent):
    if agent is None:
        return
    portrayal = {"Shape": "circle",
                 "w": 1,
                 "h": 1,
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.5}
    (x, y) = agent.pos
    portrayal["x"] = x
    portrayal["y"] = y
    portrayal["Color"] = COLORS[agent.choice]
    return portrayal