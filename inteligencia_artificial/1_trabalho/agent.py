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
        self.waitingHelp = False 
         
        if cell:
            num_agents_in_cell = sum(1 for element in cell if isinstance(element, Agent))

            for obj in cell:
                # Verifica se o objeto na célula é um recurso e se ele ainda não foi coletado
                if isinstance(obj, Resource) and not obj.collected:
                    if obj.agents_required == 1:
                        self.collecting = True
                        # Se apenas um agente é necessário, coleta o recurso
                        self.carried_resource = obj
                        obj.collected = True  
                    elif num_agents_in_cell < obj.agents_required:
                        self.waitingHelp = True
                        self.request_help(obj)
                    else:
                        # Coleta com múltiplos agentes, se disponível
                        self.collecting = True
                        collecting_agents = [element for element in cell if isinstance(element, Agent)]
                        self.carried_resource = obj  # O agente começa a carregar o recurso
                        obj.collected = True  # Marca o recurso como coletado

            self.detect_surrounding_resources(ambiente)

        
    def detect_surrounding_resources(self, ambiente):
        discovered_resources = []

        for direction, dpos in self.directions.items():
            new_x, new_y = self.x + dpos['x'], self.y + dpos['y']
            cell = ambiente.get_cell(new_x, new_y)
            if cell:
                for obj in cell:
                    if isinstance(obj, Resource) and not obj.collected:
                        discovered_resources.append(obj)

        if discovered_resources:
            self.notify_discovered_resources(discovered_resources)

    def notify_discovered_resources(self, resources):
        for resource in resources:
            print(f"Resource discovered: {resource.type} at ({resource.x}, {resource.y})")
            # Aqui você pode adicionar lógica para enviar um evento ou atualizar o ambiente

    def request_help(self, resource):
        # Criando um evento de ajuda com informações do recurso
        help_event = pygame.event.Event(pygame.USEREVENT, {
            "x": resource.x,
            "y": resource.y,
            "agents_required": resource.agents_required
        })
        pygame.event.post(help_event)

    def return_to_initial_position(self, ambiente):
        matrix = ambiente.matrix
        obstacles = {(o.x, o.y) for o in ambiente.obstacles}
        resources = [
            obj for row in matrix for cell in row for obj in cell if isinstance(obj, Resource)
        ]
        
        # Encontra o caminho para a posição inicial
        path = find_path(
            start=(self.x, self.y),
            goal=(self.initialPos['x'], self.initialPos['y']),
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
                    return True
        return False
