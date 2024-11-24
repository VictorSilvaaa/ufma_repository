import pygame
from configs import *
from utils import *
from agent import Agent

class Ambiente:
    def __init__(self, screen):
        self.screen = screen  # Tela do Pygame passada pelo init.py
        self.matrix = [[[] for _ in range(COLS)] for _ in range(ROWS)]
        self.agents = [] 
        self.resources = [] 
    
        self.populate_resources(4)  # Popula a matriz com os recursos iniciais
    
    # Popula a matriz com os recursos iniciais
    def populate_resources(self, num_resources):
        for _ in range(num_resources):
            resource = generate_random_resource(self.matrix)
            self.matrix[resource.y][resource.x] = [resource]
            self.resources.append(resource) 
        
    # Função para adicionar um recurso à matriz e à lista de recursos
    def add_element(self, element):
        pos = get_null_positon(self.matrix)
        element.x = pos['x']
        element.y = pos['y']
        if isinstance(element, Agent):
            self.agents.append(element)
        else:
            self.resources.append(element)
        self.matrix[element.y][element.x].append(element)
    
    # Limpa a matriz, removendo agentes e recursos
    def clear_matrix(self):
        for y in range(ROWS):
            for x in range(COLS):
                self.matrix[y][x] = []

    # Desenha a grid (matriz de quadrados brancos separados por linhas pretas)
    def render(self):
        self.screen.fill(WHITE)  # Limpa a tela com a cor de fundo branca

        # Limpa a matriz (removendo agentes e recursos)
        self.clear_matrix()

        # Atualiza as posições dos agentes na matriz
        for agent in self.agents: 
            if 0 <= agent.x < COLS and 0 <= agent.y < ROWS:
                self.matrix[agent.y][agent.x].append(agent)

        # Atualiza as posições dos recursos na matriz
        for resource in self.resources:
            if 0 <= resource.x < COLS and 0 <= resource.y < ROWS:
                self.matrix[resource.y][resource.x].append(resource)

        # Desenha a grid e os objetos (incluindo os agentes e recursos)
        for y in range(0, HEIGHT, GRID_SIZE):
            for x in range(0, WIDTH, GRID_SIZE):
                # Desenha o quadrado da grade
                pygame.draw.rect(self.screen, WHITE, (x, y, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(self.screen, BLACK, (x, y, GRID_SIZE, GRID_SIZE), 1)

                # Se houver objetos na posição (x, y), desenha
                cell_x = x // GRID_SIZE
                cell_y = y // GRID_SIZE
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
