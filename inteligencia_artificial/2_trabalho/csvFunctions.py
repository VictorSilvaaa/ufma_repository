import csv
from cliente import Cliente

def importClientes(): 
    clientes = []

    with open("ag_data.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            pos = row[0].split(";")
            cliente = Cliente( (int(pos[1]), int(pos[2])) )
            clientes.append(cliente)

    return clientes

import csv

def exportSolucao(aps, clientes, solucao, nome_arquivo="clientes_ap.csv"):
    with open(nome_arquivo, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        # Cabeçalho do CSV
        writer.writerow(["Cliente", "X", "Y", "AP"])

        # Escreve as linhas do CSV
        for i, cliente in enumerate(clientes):
            writer.writerow([i + 1, cliente.pos[0], cliente.pos[1], solucao[i]])

    print(f"Arquivo CSV gerado: {nome_arquivo}")

