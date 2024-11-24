#include <stdio.h>

// Definindo os registradores A, B e TEMP
unsigned int V[3];

#define A V[0]       // Registrador A
#define B V[1]       // Registrador B
#define TEMP V[2]    // Registrador temporário para ajudar na multiplicação

#define armazena_a   printf("X = "); scanf("%u", &A); B = 0;
#define armazena_b   printf("Y = "); scanf("%u", &TEMP);  // TEMP guarda o valor inicial de B
#define retorna_b    printf("Resultado da multiplicação: %u\n", B);

#define subtrai_a    if (A > 0) A = A - 1
#define adiciona_b   B = B + TEMP
#define a_zero       (A == 0)

// Programa Monolítico:
#define faca(op)     op;
#define va_para(r)   goto r;
#define se(t)        if(t)
#define entao
#define senao        else

int main() {
    armazena_a;
    armazena_b;  // Armazena TEMP como o valor de B que queremos multiplicar
    goto r0;

    r0: va_para(r1);  // Início da lógica da multiplicação

    r1: se(a_zero) entao va_para(r5) senao va_para(r2);  // Verifica se A chegou a zero
    r2: faca(subtrai_a); va_para(r3);  // Subtrai 1 de A
    r3: faca(adiciona_b); va_para(r1);  // Adiciona TEMP ao valor acumulado de B
    r5: retorna_b;  // Imprime o resultado final

    return 0;
}
