
#define F
#define G
#define T1 0
#define T2 1

#define faca(op)     op;
#define va_para(r)  goto r;
#define se(t)       if(t)
#define entao
#define senao       else

#define r0  r1

void main() {
  goto r0;

  r1: faca(F) va_para(r2)
  r2: se(T1) entao va_para(r1) senao va_para(r3)
  r3: faca(G) va_para(r4)
  r4: se(T2) entao va_para(r5) senao va_para(r1)

  r5: ;
}
