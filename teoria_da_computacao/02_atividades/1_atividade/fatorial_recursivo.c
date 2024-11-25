#include <stdio.h>
#include <stdlib.h>

// Máquina:
unsigned int V[3];
#define A V[0] // Número de entrada
#define B V[1] // Fatorial acumulado
#define C V[2] // Contador

// Operações da máquina
#define armazena_a { printf("X = "); scanf("%d", &A); B = 1; C = 1; }
#define b_multiplica_c (B *= C)
#define c_menor_igual_a (C <= A)
#define adiciona_c (C++)

// Estrutura modularizada
#define P  void main()
#define e
#define def
#define onde

// Estados e Transições
#define E0 { S(); R(); } // Fluxo inicial
#define E1 { armazena_a; } // Estado de inicialização
#define E2 { if (c_menor_igual_a) { R3(); } else { R7(); } } // Verificação da condição
#define E3 { b_multiplica_c; R4(); } // Multiplicação
#define E4 { adiciona_c; R(); } // Incremento e retorno à verificação
#define E7 { printf("Fatorial de %d = %d\n", A, B); exit(0); } // Exibe resultado e finaliza

// Declaração das funções principais
void S(); 
void R(); 
void R3(); 
void R4();
void R7();

// Função principal
P e E0 onde
void S() def E1 // Representa o estado inicial (S)
void R() def E2 // Representa o estado de verificação (R)
void R3() def E3 // Multiplicação acumulada
void R4() def E4 // Incremento e retorno
void R7() def E7 // Exibição e finalização
