#include <stdio.h>
#include <stdlib.h>

// Máquina:
unsigned int V[3];
#define A V[0] // Número de entrada
#define B V[1] // Fatorial acumulado
#define C V[2] // Contador

// Operações da máquina
#define armazena_a printf("X = "); scanf("%d", &A); B = 1; C = 1;
#define b_multiplica_c (B *= C)
#define adiciona_c (C++)

// Funções interativas
#define se(t) if (t)
#define entao
#define senao else
#define enquanto(t) while (t)
#define faca
#define ate(t) while (!(t))

void main() {
    faca armazena_a;

    enquanto(C <= A) faca {
        b_multiplica_c;
        adiciona_c;
    }

    // Exibe o resultado
    printf("Fatorial de %d = %d\n", A, B);
    exit(0);
}
