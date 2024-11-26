import random
from agent import Agent
from resource import Resource
from utils import * 

class CooperativeAgent(Agent):
    def __init__(self, x=0, y=0, id=1):
        super().__init__(x, y)
        self.img = 'Cooperativo.png'
        self.helping = False  # Indica se o agente está ajudando outro agente
        self.objectives = []
        self.name = 'Agente Cooperativo ' + str(id)

    # Mapeia todos os agentes que estão esperando por ajuda
    def calculatedHelpRequests(self, ambiente):
        waiting_agents = [
            {"x": a.x, "y": a.y, "priority": 1}  
            for a in ambiente.agents
            if a.waitingHelp == True and a != self 
        ]

        # Ordena os agentes que estão esperando por ajuda pela distância e prioridade
        waiting_agents.sort(
            key=lambda agent: (
                agent["priority"],  
                abs(self.x - agent["x"]) + abs(self.y - agent["y"]),  
            )
        )

        self.waiting_agents = waiting_agents

    def move_agent(self, ambiente):
        matrix = ambiente.matrix
        obstacles = {(o.x, o.y) for o in ambiente.obstacles}  
        
        self.calculatedHelpRequests(ambiente)

        # Se houver agentes precisando de ajuda
        if self.waiting_agents:
            nearest_agent = self.waiting_agents[0]  # Pega o agente mais próximo
            target_x, target_y = nearest_agent["x"], nearest_agent["y"]
            
            # Marca que o agente está ajudando
            self.helping = True
            
            # Calcula o caminho até o agente mais próximo
            path = find_path((self.x, self.y), (target_x, target_y), matrix, obstacles, ambiente.resources)
            if len(path)>1:
                next_step = path[1]
                self.x, self.y = next_step

                return {'x': self.x, 'y': self.y}
        
        # Se não houver agentes precisando de ajuda, o agente age como reativo
        super().move_agent(ambiente)
        return {'x': self.x, 'y': self.y}
