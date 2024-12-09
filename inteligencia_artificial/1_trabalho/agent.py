import pygame
from utils import *
from resource import Resource

class Agent:
    def __init__(self, x=None, y=None): 
        self.x = x
        self.y = y
        self.initialPos = {'x': x, 'y': y}  
        self.size = 17
        self.collecting = False
        self.color = (0, 255, 0)  
        self.speed = 5
        self.img = 'agente.png'
        self.directions = {
            "upper": {"x": 0, "y": -1}, 
            "right": {"x": 1, "y": 0}, 
            "down": {"x": 0, "y": 1}, 
            "left": {"x": -1, "y": 0},
            "upper_right": {"x": 1, "y": -1},  
            "upper_left": {"x": -1, "y": -1},  
            "down_right": {"x": 1, "y": 1},    
            "down_left": {"x": -1, "y": 1}     
        }
        self.waitingHelp = False
        self.collected_objects = [] 
        self.carried_resource = None  
        self.ambiente = None
        self.discovered_objects2 = [] 
        
         
    def detect_surrounding_resources(self):
        ambiente = self.ambiente 
        for direction, dpos in self.directions.items():
            new_x, new_y = self.x + dpos['x'], self.y + dpos['y']
            cell = ambiente.get_cell(new_x, new_y)
            if cell:
                for obj in cell:
                    if isinstance(obj, Resource) and not obj.collected and obj not in self.discovered_objects2:
                        self.discovered_objects2.append(obj)

    def move_to(self, goalPos, ambiente):
        matrix = ambiente.matrix
        obstacles = {(o.x, o.y) for o in ambiente.obstacles}
        resources = [
            obj for row in matrix for cell in row for obj in cell if isinstance(obj, Resource)
        ]
        
        # Encontra o caminho para a posição inicial
        path = find_path(
            start=(self.x, self.y),
            goal=(goalPos['x'], goalPos['y']),
            matrix=matrix,
            obstacles=obstacles,
            resources=resources,
        )
        
        if path and len(path) > 1:  
            self.x, self.y = path[1]  

        return {'x': self.x, 'y': self.y}
    
    def is_unvisited_position(self, new_x, new_y, ambiente):
        return {'x': new_x, 'y': new_y} not in ambiente.visited_pos

    def exist_resource(self, new_x, new_y, ambiente):
        cell = ambiente.get_cell(new_x, new_y)
        if cell:
            for obj in cell:
                if isinstance(obj, Resource) and not obj.collected:
                    return obj
        return False
