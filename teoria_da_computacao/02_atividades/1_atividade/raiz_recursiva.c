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

// Estrutura modularizada
#define P  void main()
#define e
#define def
#define onde

// Funções interativas
#define se(t) if (t)
#define entao
#define senao else

// Estados e Transições
#define E0 { R1(); R2(); } // Fluxo inicial
#define E1 {armazena_a; F; G; H; R2();}
#define E2 { se (T1) entao R3(); senao R4(); } // Estado E2: verifica a condição de parada
#define E3 { I; J; R2(); }                   // Estado E3: realiza a aproximação e recalcula
#define E4 { printf("Raiz quadrada de %.2f = %.6f\n", n, x); exit(0); } // Estado E4: exibe o resultado e finaliza


void R1(); 
void R2(); 
void R3(); 
void R4();
void R7();


// Função principal
P e E0 onde
void R1() def E1 // Representa o estado inicial (S)
void R2() def E2 // Representa o estado de verificação (R)
void R3() def E3 // Multiplicação acumulada
void R4() def E4 // Incremento e retorno

