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

    agents = [cooperativoAgent, objetivoAgent]
    

    ambiente.add_element(stateBasedAgent)
    ambiente.add_element(reactiveAgent)
    ambiente.add_element(cooperativoAgent)
    ambiente.add_element(objetivoAgent)

    # Variáveis de controle de tempo
    last_move_time = 0
    move_delay = 200 
    running = True

    while running:
        clock.tick(1)  

        # Verifica eventos do pygame, incluindo saída
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Chama o método handle_event apenas nos agentes que o possuem
            for agent in agents:
                if hasattr(agent, 'handle_event'):  # Verifica se o agente tem o método handle_event
                    agent.handle_event(event)

        
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_UP: 
        #             reactiveAgent.move_agent_to("upper")
        #         elif event.key == pygame.K_RIGHT: 
        #             reactiveAgent.move_agent_to("right")
        #         elif event.key == pygame.K_DOWN:  
        #             reactiveAgent.move_agent_to("down")
        #         elif event.key == pygame.K_LEFT:  
        #             reactiveAgent.move_agent_to("left")

        reactiveAgent.collect_resource(ambiente)
        stateBasedAgent.collect_resource(ambiente)
        cooperativoAgent.collect_resource(ambiente)
        objetivoAgent.collect_resource(ambiente)
       
        ambiente.render()

        for agent in agents:
            pos = agent.move_agent(ambiente) 
            # Verifica se a posição já foi visitada
            if pos not in ambiente.visited_pos:
                ambiente.visited_pos.append(pos) 
    
        pygame.display.flip()  

    pygame.quit()

if __name__ == "__main__":
    main()
