import random
from agent import Agent
from resource import Resource
from utils import *

class ObjectiveAgent(Agent):
    def __init__(self, x=0, y=0, id=1):
        super().__init__(x, y)
        self.img = 'Objetivo.png'
        self.objectives = [] 
        self.name = 'Agente Objetivo ' + str(id)

    # Mapeia todos os recursos no ambiente e retorna uma lista com suas posições
    def calculatedObjectives(self, ambiente):
        uncollected_resources = [
            r for r in ambiente.resources if r.collected == False  
        ]

        # Lista de agentes esperando ajuda com suas coordenadas e prioridade
        agents_waiting_help = [
            {"x": a.x, "y": a.y, "priority": 1}  
            for a in ambiente.agents
            if a.waitingHelp == True and a != self  
        ]

        # Remove recursos que estão na mesma posição que os agentes esperando ajuda
        uncollected_resources = [
            {
                **r.__dict__,  
                "priority": 1 if r.agents_required == 1 else 2,  
            }
            for r in uncollected_resources
            if not any(
                a["x"] == r.x and a["y"] == r.y for a in agents_waiting_help  
            )
        ]
      
        objectives = agents_waiting_help + uncollected_resources

        # Ordena os objetivos por prioridade e distância
        objectives.sort(
            key=lambda obj: (
                obj["priority"],  
                abs(self.x - obj["x"]) + abs(self.y - obj["y"]), 
            )
        )
     
        # Atualiza os recursos conhecidos do agente
        self.known_resources = objectives

    def move_agent(self, ambiente):
        if self.waitingHelp:
            print('entrou')
            return self.x, self.y 
        print('saiu')
        matrix = ambiente.matrix
        obstacles = {(o.x, o.y) for o in ambiente.obstacles}  
        self.calculatedObjectives(ambiente)

        if self.known_resources:
            nearest_resource = self.known_resources[0]
            target_x, target_y = nearest_resource["x"], nearest_resource["y"]
            
            # Calcula o caminho até o objetivo
            path = find_path((self.x, self.y), (target_x, target_y), matrix, obstacles, ambiente.resources)
            if path:
                # Verifica o próximo passo no caminho
                next_step = path[1] if len(path) > 1 else path[0]
                self.x, self.y = next_step
            
                return {'x': self.x, 'y': self.y}
        
        return {'x': self.x, 'y': self.y}
    