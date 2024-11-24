import random
from agent import Agent
from resource import Resource

class StateBasedAgent(Agent):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.img = 'stateBasedAgent.png'

    def move_agent(self, ambiente):
        if self.waitingHelp:
            return self.x, self.y  # Se o agente está esperando ajuda, ele não se move.

        directions = list(self.directions.values())
        random.shuffle(directions)  # Embaralha as direções para movimento aleatório

        # Variável para armazenar a posição de um vizinho não visitado
        posible_direction_not_visited = None
        posible_direction_visited = None

        for direction in directions:
            new_x, new_y = self.x + direction['x'], self.y + direction['y']
            
            # Verifica se a nova posição é válida dentro do ambiente
            if self.is_valid_position(new_x, new_y, ambiente):
                # Verifica se a posição ainda não foi visitada
                if self.is_unvisited_position(new_x, new_y, ambiente):
                    # Verifica se existe um recurso não coletado na posição
                    if self.exist_resource(new_x, new_y, ambiente):
                        # Move para a posição do recurso para coletá-lo
                        self.x, self.y = new_x, new_y
                        return {'x': self.x, 'y': self.y}
                    
                    # Salva uma posição não visitada para possível movimento
                    if posible_direction_not_visited is None:
                        posible_direction_not_visited = {'x': new_x, 'y': new_y}
                else:
                    # Salva uma posição visitada para possível movimento
                    if posible_direction_visited is None:
                        posible_direction_visited = {'x': new_x, 'y': new_y}

        # Se existe algum vizinho não visitado, move-se para ele
        if posible_direction_not_visited is not None:
            self.x, self.y = posible_direction_not_visited['x'], posible_direction_not_visited['y']
        else:
            self.x, self.y = posible_direction_visited['x'], posible_direction_visited['y']

        return  {'x': self.x, 'y': self.y}

    def is_unvisited_position(self, new_x, new_y, ambiente):
        return {'x': new_x, 'y': new_y} not in ambiente.visited_pos

    def exist_resource(self, new_x, new_y, ambiente):
        for obj in ambiente.matrix[new_y][new_x]:
            if isinstance(obj, Resource) and not obj.collected:
                return True
       
