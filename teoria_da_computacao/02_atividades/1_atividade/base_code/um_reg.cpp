#include <stdio.h>
#include <iostream>
using namespace std;

// Maq. um reg:
unsigned int V;

#define A  V

#define entrada   cout << "X = "; cin >> A;
#define saida     cout << "Y = " << A << "\n";

#define ad        A = A + 1
#define sub       if (A > 0) A = A - 1

#define zero      A == 0

// Programa recursivo:

#define se(t)       if(t)
#define entao
#define senao       else

void R()  {
  se(zero) entao ; senao { sub; R(); ad; ad; }
}

int main() {
  entrada;
  R();
  saida;
}
