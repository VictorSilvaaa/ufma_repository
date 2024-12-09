import pygame
from configs import *
from utils import *
from agent import Agent
import random
from obstacle import Obstacle
from resource import Resource

class Ambiente:
    def __init__(self, screen):
        self.screen = screen  
        self.matrix = [[[] for _ in range(COLS)] for _ in range(ROWS)]
        self.agents = [] 
        self.resources = [] 
        self.obstacles = []  
        self.collected_resources = []
        self.uncollected_resources = []
        self.visited_pos = []
        self.pontuacao = 0

        self.populate_obstacles(5)
        self.populate_resources(20)

    def clear_matrix(self):
        for y in range(ROWS):
            for x in range(COLS):
                self.matrix[y][x] = []
             
    def populate_obstacles(self, num_lines, fileira_tamanho=3):
        chosen_lines = random.sample(range(2, ROWS), num_lines)

        for line in chosen_lines:
            obstacle_type = random.choice(["river", "mountain"])  
            start_col = random.randint(1, COLS - fileira_tamanho)  

            for col in range(start_col, start_col + fileira_tamanho):
                obstacle = Obstacle(obstacle_type, col, line)
                self.matrix[line][col].append(obstacle)
                self.obstacles.append(obstacle)
                
    def populate_resources(self, num_resources):
        for _ in range(num_resources):
            resource = generate_random_resource(self.matrix)
            self.matrix[resource.y][resource.x].append(resource)
            self.resources.append(resource) 
    
    def get_cell(self, x, y):
        if 0 <= x < COLS and 0 <= y < ROWS:
            return self.matrix[y][x]
        return []
    
    def calculatedPontuacao(self):
        self.pontuacao = 0
        cell = self.get_cell(0, 0) 
        for obj in cell:
            if isinstance(obj, Resource):
                self.pontuacao = self.pontuacao + obj.utility

    def add_element(self, element):
        if isinstance(element, Agent):
            pos = INITIAL_POS
            element.initialPos = {'x': pos['x'], 'y': pos['y']}
            self.agents.append(element)
            element.ambiente = self
        else:
            pos = get_null_positon(self.matrix)
            if isinstance(element, Resource):
                self.resources.append(element)
            elif isinstance(element, Obstacle):
                 self.obstacles.append(element)
            
        element.x = pos['x']
        element.y = pos['y']

    def render(self):
        self.screen.fill(WHITE)  
        self.clear_matrix()

        for agent in self.agents: 
            if 0 <= agent.x < COLS and 0 <= agent.y < ROWS:
                self.matrix[agent.y][agent.x].append(agent)
        
        for resource in self.resources:
            if 0 <= resource.x < COLS and 0 <= resource.y < ROWS:
                self.matrix[resource.y][resource.x].append(resource)

        for obstacle in self.obstacles:
            if 0 <= obstacle.x < COLS and 0 <= obstacle.y < ROWS:
                self.matrix[obstacle.y][obstacle.x].append(obstacle)

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
        
        self.render_panel()

    def render_panel(self):
        self.calculatedPontuacao()
        panel_width = PANEL2_WIDTH  
        panel_x = WIDTH_T - panel_width  
        panel_y = 0  
        panel_height = HEIGHT  

        # Limpa a área do painel com a cor de fundo para não sobrepor o conteúdo anterior
        pygame.draw.rect(self.screen, WHITE_DARK, (panel_x, panel_y, panel_width, panel_height))

        font = pygame.font.Font(None, 24)
        y_offset = 20  # Posição vertical inicial para listar os recursos

        text = f"Pontucão: {self.pontuacao}"
        label = font.render(text, True, (0, 0, 0))  # Renderiza o texto
        self.screen.blit(label, (panel_x + 10, panel_y + y_offset))  # Desenha o texto na tela

                
                   

