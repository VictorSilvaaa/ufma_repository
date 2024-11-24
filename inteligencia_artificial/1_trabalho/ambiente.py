import pygame
from configs import *
from utils import *
from agent import Agent

class Ambiente:
    def __init__(self, screen):
        self.screen = screen  
        self.matrix = [[[] for _ in range(COLS)] for _ in range(ROWS)]
        self.agents = [] 
        self.resources = [] 
        self.collected_resources = []
        self.visited_pos = []
    
        self.populate_resources(4)

    def clear_matrix(self):
        for y in range(ROWS):
            for x in range(COLS):
                self.matrix[y][x] = []
             

    # Popula a matriz com os recursos iniciais
    def populate_resources(self, num_resources):
        for _ in range(num_resources):
            resource = generate_random_resource(self.matrix)
            self.matrix[resource.y][resource.x] = [resource]
            self.resources.append(resource) 
        
    def get_cell(self, x, y):
        if 0 <= x < COLS and 0 <= y < ROWS:
            return self.matrix[y][x]
        return None

    def remove_resource(self, resource):
        if resource in self.resources:
            self.resources.remove(resource)
        if 0 <= resource.x < COLS and 0 <= resource.y < ROWS:
            if resource in self.matrix[resource.y][resource.x]:
                self.matrix[resource.y][resource.x].remove(resource)
    
    def add_element(self, element):
        if isinstance(element, Agent):
            pos = INITIAL_POS
            self.agents.append(element)
            element.initialPos = {'x': pos['x'], 'y': pos['y']}
        else:
            pos = get_null_positon(self.matrix)
            self.resources.append(element)

        self.matrix[element.y][element.x].append(element)
        element.x = pos['x']
        element.y = pos['y']
        
    def render(self):
        self.screen.fill(WHITE)  # Limpa a tela com a cor de fundo branca
        self.clear_matrix()

        # Atualiza as posições dos agentes e recursos na matriz
        for agent in self.agents: 
            if 0 <= agent.x < COLS and 0 <= agent.y < ROWS:
                self.matrix[agent.y][agent.x].append(agent)
        
        for resource in self.resources:
            if 0 <= resource.x < COLS and 0 <= resource.y < ROWS:
                self.matrix[resource.y][resource.x].append(resource)

        # Desenha a grid e os objetos
        for y in range(0, HEIGHT, GRID_SIZE):
            for x in range(0, WIDTH, GRID_SIZE):
                cell_x = x // GRID_SIZE
                cell_y = y // GRID_SIZE
                pos = {"x": cell_x, "y": cell_y}

                color = WHITE
                if(cell_x == INITIAL_POS['x'] and cell_y == INITIAL_POS['y']):
                    color = RED
                elif(pos in self.visited_pos):
                    color = WHITE_DARK
                
                pygame.draw.rect(self.screen, color, (x, y, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(self.screen, BLACK, (x, y, GRID_SIZE, GRID_SIZE), 1)
                
                if len(self.matrix[cell_y][cell_x]) > 0:
                    objects = self.matrix[cell_y][cell_x]
                    num_objects = len(objects)
                    max_size = GRID_SIZE // num_objects if num_objects > 0 else GRID_SIZE
                    offset_x = 0
                    offset_y = 0
                    for obj in objects:
                        img = pygame.image.load(PATH_IMGS + obj.img)
                        img = pygame.transform.scale(img, (max_size, max_size)) 
                        self.screen.blit(img, (x + offset_x, y + offset_y))  
                        offset_x += max_size
                        if offset_x >= GRID_SIZE:
                            offset_x = 0
                            offset_y += max_size
