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
        self.waitingHelp = False
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

        if cell:
            num_agents_in_cell = sum(1 for element in cell if isinstance(element, Agent))
            for obj in cell:
                if isinstance(obj, Resource):
                    if obj.agents_required == 1:
                        # Se apenas um agente é necessário, coleta o recurso
                        ambiente.collected_resources.append({
                            'resource': obj,
                            'agents': [self]
                        })
                        obj.collected = True
                        obj.x = self.initialPos['x']
                        obj.y = self.initialPos['y']
                    elif num_agents_in_cell < 2:
                        # Se mais de um agente é necessário e há menos de dois agentes, envia um pedido de ajuda
                        self.waitingHelp = True
                        self.request_help(obj)
                    else:
                        # Coleta com múltiplos agentes, se disponível
                        collecting_agents = [element for element in cell if isinstance(element, Agent)]
                        ambiente.collected_resources.append({
                            'resource': obj,
                            'agents': collecting_agents
                        })
                        obj.collected = True
                        obj.x = self.initialPos['x']
                        obj.y = self.initialPos['y']
                        self.waitingHelp = False
    
    def request_help(self, resource):
        # Criando um evento de ajuda com informações do recurso
        help_event = pygame.event.Event(HELP_REQUEST_EVENT, {
            "x": resource.x,
            "y": resource.y,
            "agents_required": resource.agents_required
        })
        
        pygame.event.post(help_event)

    def is_valid_position(self, new_x, new_y, ambiente):
        return 0 <= new_x < len(ambiente.matrix[0]) and 0 <= new_y < len(ambiente.matrix)