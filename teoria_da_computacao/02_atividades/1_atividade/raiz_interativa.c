//ALUNO: JOÃO VICTOR DA SILVA SALES

#include <stdio.h>
#include <stdlib.h>

// Máquina:
float V[4];
#define n V[0]  // Número de entrada
#define x V[1]  // Estimativa de raiz quadrada
#define y V[2]  // Cálculo auxiliar
#define a V[3]  // Tolerância

// Operações da máquina
#define armazena_a { printf("Digite o número: "); scanf("%f", &n); }
#define F x = n       // x recebe o valor de n
#define G y = 1.0     // y inicializa com 1.0
#define H a = 0.000001 // Definindo a tolerância
#define I x = ((x + y) / 2)  // Aproximação de x
#define J y = (n / x) // Cálculo de y = n / x

#define T1 ((x - y) > a)  // Condição de parada

// Funções interativas
#define se(t) if (t)
#define entao
#define senao else
#define enquanto(t) while (t)
#define faca
#define ate(t) while (!(t))

void main() {
    faca armazena_a;  // Pede o número ao usuário

    faca F;  
    faca G;  
    faca H;  

    enquanto(T1) faca {  
        faca I;  
        faca J;  
    }

    // Exibe o resultado
    printf("Raiz quadrada de %.2f = %.6f\n", n, x);
    exit(0);
}
