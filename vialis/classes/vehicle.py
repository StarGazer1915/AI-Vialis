from mesa import Agent

class Vehicle(Agent):
    def __init__(self, pos, type, model):
        self.choice = type
        super().__init__(pos, model)
        self.pos = pos