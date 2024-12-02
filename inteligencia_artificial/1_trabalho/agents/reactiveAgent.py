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
        if self.collecting and not self.waitingHelp:
            self.return_to_initial_position(ambiente)
        else:
            self.explore_environment(ambiente)

        if self.carried_resource:
            self.carried_resource.x, self.carried_resource.y = self.x, self.y
            if self.x == self.initialPos['x'] and self.y == self.initialPos['y'] and self.carried_resource:
                self.collecting = False  
                self.carried_resource = None  

        return {'x': self.x, 'y': self.y}

    def explore_environment(self, ambiente):
        directions = list(self.directions.values())
        random.shuffle(directions)

        # Tenta mover para uma posição com um recurso não coletado
        for dpos in directions:
            new_x, new_y = self.x + dpos['x'], self.y + dpos['y']

            if is_valid_position(new_x, new_y, ambiente):
                for obj in ambiente.matrix[new_y][new_x]:
                    if isinstance(obj, Resource) and not obj.collected:
                        self.x, self.y = new_x, new_y

        # Se não encontrou um recurso, move aleatoriamente para uma posição válida
        for dpos in directions:
            new_x, new_y = self.x + dpos['x'], self.y + dpos['y']

            if is_valid_position(new_x, new_y, ambiente):
                self.x, self.y = new_x, new_y
                break

        return {'x': self.x, 'y': self.y}



