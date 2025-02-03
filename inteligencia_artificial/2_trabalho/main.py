from collections import Counter
from ap import Ap
from utils import *
from csvFunctions import *
from graficos import *

def algoritmo_genetico(aps, clientes, geracoes=100, taxa_mutacao=0.1):
    populacao = gerar_populacao(aps, clientes, 2 * len(clientes))
    fitness = [avaliar_solucao(solucao, aps, clientes) for solucao in populacao]
    
    for geracao in range(geracoes):
        nova_populacao = []
        
        for _ in range(len(populacao) // 2):  # Para cada par de pais
            pais = selecao_torneio(populacao, fitness)
            pai1, pai2 = pais[0], pais[1]
            
            # Crossover para gerar filhos
            filho1, filho2 = crossover(pai1, pai2)
            
            # Mutação nos filhos
            filho1 = mutacao(filho1, aps, taxa_mutacao)
            filho2 = mutacao(filho2, aps, taxa_mutacao)
            
            nova_populacao.extend([filho1, filho2])
        
        # Avaliar a nova população
        fitness = [avaliar_solucao(solucao, aps, clientes) for solucao in nova_populacao]
        
        # Substituir a população antiga pela nova população
        populacao = nova_populacao
        
        # Exibir informações a cada geração
        melhor_fitness = max(fitness)
        melhor_individuo = populacao[fitness.index(melhor_fitness)]
        #gerar_grafico(aps, clientes, melhor_individuo, 'melhordageracao_' + str(geracao))
        print(f"Geração {geracao + 1}: \n fitness: {melhor_fitness} \n Distancia media: {calcular_distancia_media(melhor_individuo,aps, clientes)}")
      
    
    # Retornar o melhor indivíduo
    return populacao[fitness.index(max(fitness))]

apA = Ap('A', 64, (0, 0))
apB = Ap('B', 64, (80, 0))
apC = Ap("C",  128, (0, 80))
apD = Ap("D",  128, (80, 80))
aps = [apA, apB, apC, apD]
clientes = importClientes()

algoritmo_genetico(aps, clientes)


