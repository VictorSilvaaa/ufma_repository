import random
from agent import Agent

class ReactiveAgent(Agent):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.known_resources = [{"x": x, "y": y}]
        self.lastDirection = None

    def move_agent(self, grid):
        directions = list(self.directions.keys())
        random.shuffle(directions)

        for direction in directions:
            dpos = self.directions[direction]

            new_x = self.x + dpos.x
            new_y = self.y + dpos.y

            # Verifica se a nova posição está dentro dos limites e se não há outro agente na posição
            if 0 <= new_x < len(grid[0]) and 0 <= new_y < len(grid):
                exist_agent = False
                for objects in grid[new_y][new_x]:
                    if isinstance(objects, Agent):
                        exist_agent = True

                if(not exist_agent):
                    self.x = new_x
                    self.y = new_y
                    self.known_resources.append({'x': self.x, 'y': self.y})
            
        return self.x, self.y