import os
import matplotlib.pyplot as plt

def gerar_grafico(aps, clientes, solucao, nome_arquivo="grafico.png", nome_pasta="./graficos"):
    # Garantir que a pasta exista
    if not os.path.exists(nome_pasta):
        os.makedirs(nome_pasta)  # Cria a pasta caso não exista
    
    # Criar o caminho completo para o arquivo
    caminho_arquivo = os.path.join(nome_pasta, nome_arquivo)
    
    # Criar um dicionário de cores para cada AP
    cores = {
        ap.nome: plt.cm.get_cmap('tab10')(i) 
        for i, ap in enumerate(aps)
    }
    
    # Criar a figura
    plt.figure(figsize=(10, 6))

    # Plotar clientes com cores baseadas nos APs
    for i, cliente in enumerate(clientes):
        ap = next((ap for ap in aps if ap.nome == solucao[i]), None)
        
        if ap is not None:
            cor_ap = cores[ap.nome] 
            plt.scatter(cliente.pos[0], cliente.pos[1], color=cor_ap, s=100)
        else:
            print(f"AVISO: AP não encontrado para o cliente {i+1} ({cliente.pos[0]}, {cliente.pos[1]})")
    
    # Plotar os APs como quadrados, usando suas cores
    for ap in aps:
        cor_ap = cores[ap.nome]  # Cor do AP
        plt.scatter(ap.pos[0], ap.pos[1], color=cor_ap, marker='s', s=200, label=f"AP {ap.nome}")
    
    # Ajustes no gráfico
    plt.title('Distribuição dos Clientes por AP')
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    
    # Adicionar legenda (uma entrada para cada AP)
    plt.legend(title='Pontos de Acesso', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Ajuste manual dos margens se necessário
    plt.subplots_adjust(right=0.8)  # Ajuste para garantir que a legenda não sobreponha

    # Salvar o gráfico no arquivo
    plt.savefig(caminho_arquivo, bbox_inches='tight')  # Salvando o gráfico no arquivo

    print(f"Gráfico salvo em {caminho_arquivo}")
