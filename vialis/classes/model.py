from mesa import Model
from mesa.time import RandomActivation
from mesa.space import Grid

from mesa.datacollection import DataCollector

from vialis.classes.empty import Empty
from vialis.classes.vehicle import Vehicle

class Vialis(Model):
    def __init__(self, height=100, width=100):
        # Set up model objects
        self.schedule = RandomActivation(self)
        self.grid = Grid(height, width, torus=False)

        self.datacollector = DataCollector(
            {
                "None": lambda m: self.count_type(m, "None"),
                "Car": lambda m: self.count_type(m, "Car"),
                "Bus": lambda m: self.count_type(m, "Bus")
            }
        )

        for (contents, x, y) in self.grid.coord_iter():
            # Create a voter.
            if x == 20 and y == 20:
                new_agent = Vehicle((x, y), "Car", self)
            elif x == 80 and y == 80:
                new_agent = Vehicle((x, y), "Bus", self)
            else:
                new_agent = Empty((x, y), self)
            self.grid._place_agent((x, y), new_agent)
            self.schedule.add(new_agent)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Advance the model by one step.
        """
        self.schedule.step()
        # collect data.
        self.datacollector.collect(self)

    @staticmethod
    def count_type(model, voter_choice):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for voter in model.schedule.agents:
            if voter.choice == voter_choice:
                count += 1
        return count