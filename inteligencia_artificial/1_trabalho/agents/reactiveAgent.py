import random
from agent import Agent
from utils import *
from resource import Resource

class ReactiveAgent(Agent):
    def __init__(self, x=0, y=0, id=1):
        super().__init__(x, y)
        self.known_resources = [] 
        self.lastDirection = None  
        self.name = f'Agente Reativo {id}'
        
    def move_agent(self, ambiente):
        if self.collecting:
            self.move_to(self.initialPos, ambiente)
        else:
            self.explore_environment(ambiente)

        return {'x': self.x, 'y': self.y}

    def explore_environment(self, ambiente):
        directions = list(self.directions.values())
        random.shuffle(directions)

        for direction in directions:
            new_x, new_y = self.x + direction['x'], self.y + direction['y']

            if is_valid_position(new_x, new_y, ambiente) and self.is_position_of_interest(new_x, new_y):
                self.x, self.y = new_x, new_y
                return {'x': self.x, 'y': self.y}

        # Se não encontrou um recurso, move aleatoriamente para uma posição válida
        for dpos in directions:
            new_x, new_y = self.x + dpos['x'], self.y + dpos['y']
            if is_valid_position(new_x, new_y, ambiente) and new_x != 0 and new_y != 0:
                self.x, self.y = new_x, new_y
                break

        return {'x': self.x, 'y': self.y}

    def collect_resource(self, ambiente):
        if(self.collecting):
            if(self.x == 0 and self.y == 0):
                self.carried_resource = None
                self.collecting = False
        else:
            cell = ambiente.get_cell(self.x, self.y)
            for obj in cell:
                if isinstance(obj, Resource) and obj.utility == 10 and not obj.collected:
                    self.collecting = True
                    obj.collected = True
                    self.carried_resource = obj
                    break
        
        self.detect_surrounding_resources()

    def is_position_of_interest(self, x, y):
        cell = self.ambiente.get_cell(x, y)
        for obj in cell:
            if isinstance(obj, Resource) and obj.utility == 10 and not obj.collected:
                return True
        return False
