import pygame
import random
from utils import convert_to_grid_pos

class Agent:
    def __init__(self, x, y): 
        self.x = x
        self.y = y
        self.size = 17
        self.color = (0, 255, 0)  
        self.speed = 5
        self.img = 'agente.png'

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

    def draw(self, screen):
        agent_x, agent_y = convert_to_grid_pos(self.x, self.y)
        pygame.draw.circle(screen, self.color, (agent_x, agent_y), self.size)

    def check_collision(self, resource):
        # Verifica colisão entre o agente e um recurso
        distance = ((self.x - resource["x"]) ** 2 + (self.y - resource["y"]) ** 2) ** 0.5
        return distance < (self.size + resource["info"]["size"])
