import pygame
from ambiente import Ambiente
from agent import Agent
from agents.reactiveAgent import ReactiveAgent
from agents.stateBasedAgent import StateBasedAgent
from agents.cooperativeAgent import CooperativeAgent
from agents.objectiveAgent import ObjectiveAgent
from configs import *

def main():
    # Inicialização do Pygame
    pygame.init()  
    screen = pygame.display.set_mode((WIDTH_T, HEIGHT_T)) 
    pygame.display.set_caption("Agente Explorador - Coleta de Recursos")  
    clock = pygame.time.Clock() 

    # Criação do ambiente e inicialização dos agentes
    ambiente = Ambiente(screen)  

    reactiveAgent = ReactiveAgent()
    stateBasedAgent = StateBasedAgent()
    cooperativoAgent = CooperativeAgent()
    objetivoAgent = ObjectiveAgent()

    agents = [reactiveAgent, stateBasedAgent, objetivoAgent]
    for agent in agents:
            ambiente.add_element(agent)

    running = True
    while running:
        clock.tick(1)  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for agent in agents:
            agent.collect_resource(ambiente)

        ambiente.render()

        for agent in agents:
            pos = agent.move_agent(ambiente) 
            if pos not in ambiente.visited_pos:
                ambiente.visited_pos.append(pos) 
    
        pygame.display.flip()  

    pygame.quit()

if __name__ == "__main__":
    main()
