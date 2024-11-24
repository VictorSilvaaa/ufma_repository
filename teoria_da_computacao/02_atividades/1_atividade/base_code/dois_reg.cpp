#include <stdio.h>
#include <iostream>
using namespace std;

// Maq. dois reg:
unsigned int V[2];

#define A  V[0]
#define B  V[1]

#define armazena_a   cout << "X = "; cin >> A; B = 0;
#define retorna_b    cout << "Y = " << B << "\n";

#define subtrai_a    if (A > 0) A = A - 1
#define adiciona_b   B = B + 1

#define a_zero       A == 0


// Programa Monolítico:
#define faca(op)     op;
#define va_para(r)  goto r;
#define se(t)       if(t)
#define entao
#define senao       else


// Computação

#define par(r)     printf("(r%d; (A: %d, B: %d))\n", r, A, B)

int f () {
  return f();
}

int main() {
  f();

  armazena_a;

  r1: par(1); se(a_zero) entao va_para(r9) senao va_para(r2)
  r2: par(2); faca(subtrai_a)  va_para(r3)
  r3: par(3); faca(adiciona_b) va_para(r1)
  r9: par(9);

  retorna_b;
}
