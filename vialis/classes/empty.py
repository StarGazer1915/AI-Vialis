from mesa import Agent

class Empty(Agent):
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos
        self.choice = "None"