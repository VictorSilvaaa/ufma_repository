import pygame
from utils import convert_to_grid_pos
from configs import *
from resource import Resource

class Agent:
    def __init__(self, x=None, y=None): 
        self.x = x
        self.y = y
        self.initialPos = {'x' : x, 'y' : y}  
        self.size = 17
        self.color = (0, 255, 0)  
        self.speed = 5
        self.img = 'agente.png'
        self.directions = {
            "upper" : {"x": 0, "y": -1}, 
            "right": {"x": 1, "y": 0}, 
            "down": {"x": 0, "y": 1}, 
            "left": {"x": -1, "y": 0}
        }
        self.collected_objects = []  

    def draw(self, screen):
        agent_x, agent_y = convert_to_grid_pos(self.x, self.y)
        pygame.draw.circle(screen, self.color, (agent_x, agent_y), self.size)

    def move_agent_to(self, direction):
        if direction in self.directions:
            dpos = self.directions[direction]
            self.x += dpos['x']
            self.y += dpos['y']
        return self.x, self.y         

    def collect_resource(self, ambiente):
        cell = ambiente.get_cell(self.x, self.y)
        for object in cell:
            if cell and isinstance(cell[0], Resource):
                self.collected_objects.append(cell[0])
                object.x = self.initialPos['x']
                object.y = self.initialPos['y']
