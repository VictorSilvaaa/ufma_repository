import random
from agent import Agent
from resource import Resource

class ReactiveAgent(Agent):
    def __init__(self, x=0, y=0, id=1):
        super().__init__(x, y)
        self.known_resources = [{"x": x, "y": y}]
        self.lastDirection = None
        self.name = 'Agente Reativo ' + str(id)

    

