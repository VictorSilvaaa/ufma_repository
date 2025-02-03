#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define POP_SIZE 10    // Tamanho da população
#define NUM_ITEMS 5    // Número de itens disponíveis
#define MAX_CAPACITY 50 // Capacidade máxima da bolsa
#define MASTER 0

// Estrutura de item do PUBG
typedef struct {
    char name[20];
    int space;
    int utility;
} Item;

// Itens disponíveis no jogo
Item items[NUM_ITEMS] = {
    {"Arma AKM", 10, 50},
    {"Colete Nível 3", 15, 70},
    {"Mochila Nível 3", 20, 80},
    {"Kit Médico", 5, 40},
    {"Granada", 2, 20}
};

// Representação de um indivíduo
typedef struct {
    int genes[NUM_ITEMS];
    int fitness;
} Individual;

// Função para calcular fitness
total int calculate_fitness(Individual *ind) {
    int total_utility = 0, total_space = 0;
    for (int i = 0; i < NUM_ITEMS; i++) {
        if (ind->genes[i]) {
            total_utility += items[i].utility;
            total_space += items[i].space;
        }
    }
    return (total_space <= MAX_CAPACITY) ? total_utility : 0;
}

// Função para inicializar um indivíduo aleatoriamente
void initialize_individual(Individual *ind) {
    for (int i = 0; i < NUM_ITEMS; i++) {
        ind->genes[i] = rand() % 2; // 0 ou 1 para incluir ou não o item
    }
    ind->fitness = 0;
}

int main(int argc, char** argv) {
    int rank, size;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    Individual population[POP_SIZE];
    Individual best_individual;
    best_individual.fitness = 0;
    
    if (rank == MASTER) {
        srand(time(NULL));
        // Inicializa a população
        for (int i = 0; i < POP_SIZE; i++) {
            initialize_individual(&population[i]);
        }
        
        // Distribuir indivíduos para os escravos avaliarem
        for (int i = 0; i < POP_SIZE; i++) {
            MPI_Send(&population[i], sizeof(Individual), MPI_BYTE, (i % (size - 1)) + 1, 0, MPI_COMM_WORLD);
        }
        
        // Receber fitness dos escravos
        for (int i = 0; i < POP_SIZE; i++) {
            MPI_Recv(&population[i], sizeof(Individual), MPI_BYTE, MPI_ANY_SOURCE, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            if (population[i].fitness > best_individual.fitness) {
                best_individual = population[i];
            }
        }
        
        printf("Melhor combinação de itens: \n");
        for (int i = 0; i < NUM_ITEMS; i++) {
            if (best_individual.genes[i]) {
                printf("%s\n", items[i].name);
            }
        }
        printf("Fitness: %d\n", best_individual.fitness);
    } else {
        // Escravo recebe indivíduos, avalia e envia de volta
        Individual ind;
        for (int i = 0; i < POP_SIZE / (size - 1); i++) {
            MPI_Recv(&ind, sizeof(Individual), MPI_BYTE, MASTER, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            ind.fitness = calculate_fitness(&ind);
            MPI_Send(&ind, sizeof(Individual), MPI_BYTE, MASTER, 0, MPI_COMM_WORLD);
        }
    }
    
    MPI_Finalize();
    return 0;
}
