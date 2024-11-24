
// maquina de dois regs:

unsigned int  a, b;

void armazena_a(unsigned x) {
  a = x;
  b = 0;
}

unsigned retorna_b() {
  return b;
}

void subtrai_a() {
  if (a > 0)  a = a - 1;
}

void incrementa_b() {
  b = b + 1;
}

int a_zero() {
  return a == 0;
}


// Interpretação
#define F   subtrai_a()
#define G   incrementa_b()
#define T   a_zero()


// Programa
void S();
void R();


#define se(t)       if(t)
#define entao
#define senao       else

#define P  void main()
#define e
#define def
#define onde

#define E0 {R; S;}
#define E1 {F; se(T) entao R; senao G;S;}

P e E0 onde
void S() def E1
void R() def E1
