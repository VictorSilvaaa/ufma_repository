from agent import Agent

class StateBasedAgent(Agent):
    def __init__(self, name, pos):
        super().__init__(name, pos)
        self.visited = set() 

    def act(self, grid, turn, known_resources, other_agents):
        if turn > 1:
            direction = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
            while True:
                new_pos = move_agent(grid, self.pos, direction)
                if new_pos not in self.visited:
                    self.pos = new_pos
                    self.visited.add(self.pos)
                    resource = grid[self.pos[0]][self.pos[1]]
                    if resource not in known_resources:
                        known_resources.append(self.pos) 
                    
                    collected = collect_resource(grid, self.pos, allowed_resources=['Cristais Energéticos', 'Blocos de Metal Raro'])
                    if collected:
                        self.inventory.append(collected)
                    break
                else:
                    direction = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])