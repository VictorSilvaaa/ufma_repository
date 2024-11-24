import pygame
from configs import *
from utils import generate_random_resource
from agent import Agent

class Ambiente:
    def __init__(self):
        # Configuração inicial do pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Agente Explorador - Coleta de Recursos")
        self.clock = pygame.time.Clock()
        
        self.matrix = [[[] for _ in range(COLS)] for _ in range(ROWS)]
    
        self.populate_resources(4)  
    
    # Popula a matriz com os recursos iniciais
    def populate_resources(self, num_resources):
        for _ in range(num_resources):
            resource = generate_random_resource(self.matrix)
            self.matrix[resource.y][resource.x].append(resource)

    # Desenha a grid (matriz de quadrados brancos separados por linhas pretas)
    def render(self):
        self.screen.fill(WHITE)

        for y in range(0, HEIGHT, GRID_SIZE):
            for x in range(0, WIDTH, GRID_SIZE):
                pygame.draw.rect(self.screen, WHITE, (x, y, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(self.screen, BLACK, (x, y, GRID_SIZE, GRID_SIZE), 1)

                # Se houver objetos na posição (x, y), desenha
                if len(self.matrix[y // GRID_SIZE][x // GRID_SIZE]) > 0:
                    objects = self.matrix[y // GRID_SIZE][x // GRID_SIZE]
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

        pygame.display.flip()

