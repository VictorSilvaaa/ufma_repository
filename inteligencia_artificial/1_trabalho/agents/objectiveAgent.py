import random
from agent import Agent
from resource import Resource
from utils import *
from agents.reactiveAgent import ReactiveAgent

class ObjectiveAgent(Agent):
    def __init__(self, x=0, y=0, id=1):
        super().__init__(x, y)
        self.img = 'Objetivo.png'
        self.name = 'Agente Objetivo ' + str(id)
        self.objectives = [] 
        self.uncollected_resources = []

    # Mapeia todos os recursos no ambiente e retorna uma lista com suas posições
    def calculatedObjectives(self):
        discovered = [obj for obj in self.uncollected_resources if not obj.collected]
        uncollected_resources = [
            {"x": r.x, "y": r.y, "priority": 1}  
            for r in discovered
        ]
      
        objectives = uncollected_resources

        # Ordena os objetivos por prioridade e distância
        objectives.sort(
            key=lambda obj: (
                obj["priority"],  
                abs(self.x - obj["x"]) + abs(self.y - obj["y"]), 
            )
        )
     
        # Atualiza os recursos conhecidos do agente
        self.objectives = objectives

    def move_agent(self, ambiente):
        if(not self.waitingHelp):
            if self.collecting:
                self.move_to(self.initialPos, ambiente) 
            else:
                if(len(self.objectives) == 0):
                    self.explore_environment(ambiente)
                else:
                    print(self.objectives[0])
                    next_step = self.objectives[0]
                    self.move_to(next_step, ambiente)

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
                elif self.is_unvisited_position(new_x, new_y, ambiente):
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
        self.calculatedObjectives()

        if(self.waitingHelp):
            if(len(self.objectives) == 0):
                for obj in cell:
                    if isinstance(obj, Resource):
                        if(num_agents >= obj.agents_required):
                            self.waitingHelp = False
                            break
            else:
                self.collecting = False
                self.waitingHelp = False

        if(self.collecting):
            if(self.x == 0 and self.y == 0):
                self.carried_resource = None
                self.collecting = False
                self.waitingHelp = False
        else:
            for obj in cell:
                if isinstance(obj, Resource) and not obj.collected:
                    if(num_agents >= obj.agents_required):
                        self.collecting = True
                        obj.collected = True
                        self.carried_resource = obj
                        self.waitingHelp = False
                        break
                    else:
                        num_agents_can_help = sum(1 for obj in self.ambiente.agents if isinstance(obj, Agent) and not isinstance(obj, ReactiveAgent)) 
                        if num_agents_can_help >= obj.agents_required:
                            self.collecting = True
                            self.waitingHelp = True
                        break
        
        self.detect_surrounding_resources()