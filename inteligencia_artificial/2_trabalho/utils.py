import random
import numpy as np
import pygame

# Função para calcular a distância entre dois pontos
def calcular_distancia(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

# Função de avaliação (fitness)
def avaliar_solucao(solucao, aps, clientes):
    fitness_total = 0
    capacidades = {ap.nome: 0 for ap in aps}
    
    for i, ap_nome in enumerate(solucao):
        cliente = clientes[i]
        ap = next((ap for ap in aps if ap.nome == ap_nome), None)
        
        if ap:
            distancia = calcular_distancia(cliente.pos, ap.pos)
            fitness_total += 1 / (distancia + 1)  
            
            capacidades[ap_nome] += 1
            
            # Penaliza se o número de clientes conectados exceder a capacidade do AP
            if capacidades[ap_nome] > ap.capacidade:
                fitness_total -= 100  # Penaliza fortemente soluções inválidas

    return fitness_total

def gerar_populacao(aps, clientes, tamanho_populacao=50): 
    populacao = []
    
    for _ in range(tamanho_populacao):
        individuo = []
        clientes_conectados = {ap.nome: 0 for ap in aps}

        for cliente in clientes:
            ap_selecionado = random.choice([ap for ap in aps if clientes_conectados[ap.nome] < ap.capacidade])
            individuo.append(ap_selecionado.nome)
            
            clientes_conectados[ap_selecionado.nome] += 1
        
        populacao.append(individuo)  
    
    return populacao

def calcular_distancia_media(solucao, aps, clientes):
    distancias = []
    
    # Para cada cliente, encontra o AP ao qual está atribuído e calcula a distância
    for i, ap_nome in enumerate(solucao):
        cliente = clientes[i]
        ap_obj = next((ap for ap in aps if ap.nome == ap_nome), None)
        
        if ap_obj:
            # Calcula a distância entre o cliente e o AP
            distancia = calcular_distancia(cliente.pos, ap_obj.pos)
            distancias.append(distancia)
    
    # Retorna a distância média
    return sum(distancias) / len(distancias) if distancias else 0

def selecao_torneio(populacao, fitness, tamanho_torneio=None):
    pais = []
    
    if tamanho_torneio is None:
        tamanho_torneio = len(populacao) // 6
    
    for _ in range(2):  # Selecionar dois pais
        torneio = random.sample(range(len(populacao)), tamanho_torneio)  # Seleção de um torneio de tamanho_torneio
        
        # Ordenar os índices do torneio baseado no fitness e pegar os melhores
        melhores = sorted(torneio, key=lambda i: fitness[i], reverse=True)
        
        # Adicionar o melhor indivíduo ao pool de pais
        pais.append(populacao[melhores[0]])  
    
    return pais

# Crossover: Cruzamento de dois pais
def crossover(pai1, pai2):
    ponto_corte = random.randint(1, len(pai1) - 1)  # Escolher ponto de corte aleatório
    filho1 = pai1[:ponto_corte] + pai2[ponto_corte:]
    filho2 = pai2[:ponto_corte] + pai1[ponto_corte:]
    return filho1, filho2

# Mutação: Introduzir mutações aleatórias
def mutacao(individuo, aps, taxa_mutacao=0.1):
    for i in range(len(individuo)):
        if random.random() < taxa_mutacao:  # Se o valor aleatório for menor que a taxa de mutação
            ap_atual = individuo[i]  # O AP atual do cliente
            ap_novo = random.choice([ap for ap in aps if ap.nome != ap_atual])  # Escolhe um AP diferente
            individuo[i] = ap_novo.nome  # Atribui o novo AP
    return individuo


