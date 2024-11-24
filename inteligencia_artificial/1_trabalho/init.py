import pygame
from ambiente import Ambiente
from agent import Agent

def main():
    ambiente = Ambiente()

    # Variáveis de controle de tempo
    last_move_time = 0
    move_delay = 200  # Milissegundos de atraso para movimento do agente
    running = True

    # Controlador de tempo
    time = pygame.time.Clock()

    # Loop principal do jogo
    while running:
        time.tick(30)

        # Verifica eventos do pygame, incluindo saída
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Atualiza o ambiente visual
        ambiente.render()

    pygame.quit()

if __name__ == "__main__":
    main()
