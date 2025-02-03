from collections import Counter
from ap import Ap
from utils import *
from csvFunctions import *
from graficos import *

def algoritmo_genetico(aps, clientes, geracoes=1000, taxa_mutacao_gene=0.05, taxa_mutacao_filho=0.25):
    # Gerar população inicial e calcular o fitness
    populacao = gerar_populacao(aps, clientes, 4 * len(clientes))
    fitness = [avaliar_solucao(solucao, aps, clientes) for solucao in populacao]

    for geracao in range(geracoes):
        nova_populacao = []
        
        # Guardar o melhor indivíduo da população atual
        indice_melhor_fitness_atual = max(range(len(fitness)), key=lambda i: fitness[i])
        melhor_individuo_atual = populacao[indice_melhor_fitness_atual]

        #gerar_grafico(aps, clientes, melhor_individuo_atual, 'melhordageracao_' + str(geracao))
        print(f"Geração {geracao + 1}: \n Distancia media: {calcular_distancia_media(melhor_individuo_atual, aps, clientes)}")
        
        # Garantir que o melhor indivíduo esteja na próxima geração
        nova_populacao.append(melhor_individuo_atual) 
        
        # Gerar a nova população com crossover e mutação
        for _ in range(len(populacao) // 2):  
            pais = selecao_torneio(populacao, fitness)
            pai1, pai2 = pais[0], pais[1]
            
            # Crossover para gerar filhos
            filho1, filho2 = crossover(pai1, pai2)
            
            # Mutação nos filhos
            if random.random() <= taxa_mutacao_filho:
                filho1 = mutacao(filho1, aps, taxa_mutacao_gene)
            if random.random() <= taxa_mutacao_filho:
                filho2 = mutacao(filho2, aps, taxa_mutacao_gene)
            
            nova_populacao.extend([filho1, filho2])
        
        fitness = [avaliar_solucao(solucao, aps, clientes) for solucao in nova_populacao]
        populacao = nova_populacao
        
    
    return populacao[fitness.index(max(fitness))]

apA = Ap('A', 64, (0, 0))
apB = Ap('B', 64, (80, 0))
apC = Ap("C",  128, (0, 80))
apD = Ap("D",  128, (80, 80))
aps = [apA, apB, apC, apD]
clientes = importClientes()

algoritmo_genetico(aps, clientes)


