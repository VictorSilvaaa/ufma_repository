import random
from agent import Agent
from resource import Resource

class ReactiveAgent(Agent):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.known_resources = [{"x": x, "y": y}]
        self.lastDirection = None

    def move_agent(self, ambiente):
        matrix = ambiente.matrix
        if not self.waitingHelp:
            directions = list(self.directions.values())
            random.shuffle(directions)

            # Tenta mover para uma posição com um recurso não coletado
            for dpos in directions:
                new_x, new_y = self.x + dpos['x'], self.y + dpos['y']

                if 0 <= new_x < len(matrix[0]) and 0 <= new_y < len(matrix):
                    for obj in matrix[new_y][new_x]:
                        if isinstance(obj, Resource) and not obj.collected:
                            self.x, self.y = new_x, new_y
                            return {'x': self.x, 'y': self.y}

            # Se não encontrou um recurso, move aleatoriamente para uma posição válida
            for dpos in directions:
                new_x, new_y = self.x + dpos['x'], self.y + dpos['y']

                if 0 <= new_x < len(matrix[0]) and 0 <= new_y < len(matrix):
                    if not any(isinstance(obj, Resource) and obj.collected for obj in matrix[new_y][new_x]):
                        self.x, self.y = new_x, new_y
                        break

        return {'x': self.x, 'y': self.y}


