import random
import pygame
from agent import Agent
from resource import Resource

class CooperativoAgent(Agent):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.img = 'Cooperativo.png'
        self.known_resources = [{"x": x, "y": y}]
        self.lastDirection = None
        self.help_target = None  # Variável para armazenar as coordenadas do evento de ajuda

    def handle_event(self, event):
        """ Lida com o evento de ajuda e define o alvo de movimento. """
        if event.type == pygame.USEREVENT + 1:  # Evento de ajuda
            self.help_target = (event.dict['x'], event.dict['y'])  # Armazena o alvo do evento

    def move_agent(self, ambiente):
        matrix = ambiente.matrix

        # Se o agente está esperando ajuda, move-se em direção ao alvo
        if self.help_target:
            target_x, target_y = self.help_target

            # Move o agente em direção ao alvo (evento de ajuda)
            if self.x < target_x:
                self.x += 1
            elif self.x > target_x:
                self.x -= 1
            elif self.y < target_y:
                self.y += 1
            elif self.y > target_y:
                self.y -= 1

            # Verifica se o agente chegou no alvo
            if self.x == target_x and self.y == target_y:
                self.help_target = None  # Desativa o alvo, já chegou

        else:
            # Lógica normal de movimento, se não houver um alvo de ajuda
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
