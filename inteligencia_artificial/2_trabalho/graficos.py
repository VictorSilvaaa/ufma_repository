import os
import matplotlib.pyplot as plt

def gerar_grafico(aps, clientes, solucao, nome_arquivo="grafico.png", pasta_destino="graficos"):
    # Verificar se a pasta existe, se não, criar
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    # Construir o caminho completo do arquivo
    caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
    
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
        cor_ap = cores[ap.nome]  
        # Plotando os clientes com a cor do AP correspondente
        plt.scatter(cliente.pos[0], cliente.pos[1], color=cor_ap, s=100)

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

    # Salvar o gráfico no arquivo no caminho especificado
    plt.savefig(caminho_arquivo, bbox_inches='tight')  # Salvando o gráfico no arquivo

    print(f"Gráfico salvo em {caminho_arquivo}")

# Exemplo de uso:
# gerar_grafico(aps, clientes, solucao, pasta_destino="graficos/resultado", nome_arquivo="grafico_clientes.png")
