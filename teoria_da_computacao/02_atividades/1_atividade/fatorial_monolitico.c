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
#define c_menor_igual_a (C <= A)
#define adiciona_c (C++)

// Programação monolítica
#define faca(op) op;
#define va_para(r) goto r;
#define se(t) if (t)
#define entao
#define senao else

void main() {
    va_para(r1); 

    r1: faca(armazena_a) va_para(r2);
    r2: se(c_menor_igual_a) entao va_para(r3) senao va_para(r7);
    r3: faca(b_multiplica_c) va_para(r4);
    r4: faca(adiciona_c) va_para(r2);
    r7: ;

    // Exibe o resultado
    printf("Fatorial de %d = %d\n", A, B);
    exit(0);
}