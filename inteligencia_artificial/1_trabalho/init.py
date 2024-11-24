import pygame
from ambiente import Ambiente
from agent import Agent
from agents.reactiveAgent import ReactiveAgent
from configs import *

def main():
    # Inicialização do Pygame
    pygame.init()  
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
    pygame.display.set_caption("Agente Explorador - Coleta de Recursos")  
    clock = pygame.time.Clock() 

    # Criação do ambiente e inicialização dos agentes
    ambiente = Ambiente(screen)  
    reactiveAgent = ReactiveAgent()
    ambiente.add_element(reactiveAgent)

    # Variáveis de controle de tempo
    last_move_time = 0
    move_delay = 200 
    running = True

    while running:
        clock.tick(30)  

        # Verifica eventos do pygame, incluindo saída
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: 
                    reactiveAgent.move_agent_to("up")
                elif event.key == pygame.K_RIGHT: 
                    reactiveAgent.move_agent_to("right")
                elif event.key == pygame.K_DOWN:  
                    reactiveAgent.move_agent_to("down")
                elif event.key == pygame.K_LEFT:  
                    reactiveAgent.move_agent_to("left")

        ambiente.render()

        pygame.display.flip()  

    pygame.quit()

if __name__ == "__main__":
    main()
