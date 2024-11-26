//ALUNO: JOÃO VICTOR DA SILVA SALES

#include <stdio.h>
#include <stdlib.h>

float V[4];

#define n V[0]
#define x V[1]
#define y V[2]
#define a V[3]

// Definindo as operações da máquina
#define armazena_a { printf("Digite o número: "); scanf("%f", &n); }  // Lê o número
#define F x = n            // x recebe o valor de n
#define G y = 1.0          // y inicializa com 1.0
#define H a = 0.000001     // Definindo a tolerância para a diferença
#define I x = ((x + y) / 2) // Aproximação de x
#define J y = (n / x)      // Cálculo de y = n / x

#define T1 ((x - y) > a)   // Condição de parada

#define faca(op)     op;
#define va_para(r)   goto r;
#define se(t)        if(t)
#define entao
#define senao        else

void main() {
  va_para(r0); // Inicia o fluxo na rotina r0

  r0: faca(armazena_a) va_para(r1); 
  r1: faca(F) va_para(r2);          
  r2: faca(G) va_para(r3);         
  r3: faca(H) va_para(r4);         
  r4: se(T1) entao va_para(r5) senao va_para(r9); 
  r5: faca(I) va_para(r6);          
  r6: faca(J) va_para(r4);          
  r9: ;

  // Exibe o resultado
  printf("Raiz quadrada de %.2f = %.6f\n", n, x);
  exit(0);
}
