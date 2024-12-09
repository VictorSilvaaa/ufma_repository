import random
from agent import Agent
from utils import *
from resource import Resource
from agents.reactiveAgent import ReactiveAgent

class StateBasedAgent(Agent):
    def __init__(self, x=0, y=0, id=1):
        super().__init__(x, y)
        self.img = 'stateBasedAgent.png'
        self.name = f'Agente Estado {id}'
        self.uncollected_resources = []

    def move_agent(self, ambiente):
        if(not self.waitingHelp):
            if self.collecting:
                self.move_to(self.initialPos, ambiente)
            else:
                self.explore_environment(ambiente)

        return {'x': self.x, 'y': self.y}

    def explore_environment(self, ambiente):
        directions = list(self.directions.values())
        random.shuffle(directions) 

        possible_unvisited = None
        possible_visited = None
        for direction in directions:
            new_x, new_y = self.x + direction['x'], self.y + direction['y']
            if is_valid_position(new_x, new_y, ambiente):
                if self.is_position_of_interest(new_x, new_y):
                    self.x, self.y = new_x, new_y
                    return {'x': self.x, 'y': self.y}
                elif new_x !=0 and new_y !=0:
                    if self.is_unvisited_position(new_x, new_y, ambiente):
                        if possible_unvisited is None:
                            possible_unvisited = {'x': new_x, 'y': new_y}
                    else:
                        if possible_visited is None:
                            possible_visited = {'x': new_x, 'y': new_y}

        # Prioriza posições não visitadas; caso contrário, move para posições visitadas
        if possible_unvisited:
            self.x, self.y = possible_unvisited['x'], possible_unvisited['y']
        elif possible_visited:
            self.x, self.y = possible_visited['x'], possible_visited['y']

        return {'x': self.x, 'y': self.y}
    
    def is_position_of_interest(self, x, y):
        cell = self.ambiente.get_cell(x, y)
        num_agents_can_help = sum(1 for obj in self.ambiente.agents if isinstance(obj, Agent) and not isinstance(obj, ReactiveAgent)) 
        for obj in cell:
            if isinstance(obj, Resource) and not obj.collected and num_agents_can_help >= obj.agents_required:
                return True
        return False
    
    def collect_resource(self, ambiente):
        cell = ambiente.get_cell(self.x, self.y)
        num_agents = sum(1 for obj in cell if isinstance(obj, Agent) and not isinstance(obj, ReactiveAgent))

        if(self.waitingHelp):
            for obj in cell:
                if isinstance(obj, Resource):
                    if(num_agents >= obj.agents_required):
                        self.waitingHelp = False
                        break

        if(self.collecting):
            if(self.x == 0 and self.y == 0):
                self.carried_resource = None
                self.collecting = False
        else:
            for obj in cell:
                if isinstance(obj, Resource) and not obj.collected:
                    if(num_agents >= obj.agents_required):
                        self.collecting = True
                        obj.collected = True
                        self.carried_resource = obj
                        break
                    else:
                        num_agents_can_help = sum(1 for obj in self.ambiente.agents if isinstance(obj, Agent) and not isinstance(obj, ReactiveAgent)) 
                        if num_agents_can_help >= obj.agents_required:
                            self.collecting = True
                            self.waitingHelp = True
                        break
        
        self.detect_surrounding_resources()