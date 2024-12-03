import random
from agent import Agent
from utils import *
from resource import Resource

class StateBasedAgent(Agent):
    def __init__(self, x=0, y=0, id=1):
        super().__init__(x, y)
        self.img = 'stateBasedAgent.png'
        self.name = f'Agente Estado {id}'

    def move_agent(self, ambiente):
        if self.waitingHelp:
            return {'x': self.x, 'y': self.y}
        if self.collecting:
            self.move_to(self.initialPos, ambiente)
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

        # Variáveis para armazenar possíveis movimentos
        possible_unvisited = None
        possible_visited = None

        for direction in directions:
            new_x, new_y = self.x + direction['x'], self.y + direction['y']

            # Verifica se a nova posição é válida dentro do ambiente
            if is_valid_position(new_x, new_y, ambiente):
                # Verifica se existe um recurso não coletado na posição
                if self.exist_resource(new_x, new_y, ambiente):
                    # Move para a posição do recurso para coletá-lo
                    self.x, self.y = new_x, new_y
                    return {'x': self.x, 'y': self.y}

                # Verifica se a posição ainda não foi visitada
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

        # Marca a posição atual como visitada
        ambiente.visited_pos.append({'x': self.x, 'y': self.y})

        # Atualiza a posição do recurso carregado, se houver
        if self.carried_resource:
            self.carried_resource.x, self.carried_resource.y = self.x, self.y

        return {'x': self.x, 'y': self.y}