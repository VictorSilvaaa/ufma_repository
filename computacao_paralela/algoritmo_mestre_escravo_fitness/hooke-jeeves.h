double Simplex(double (*func)(double[], int n), double start[], double fstart,
               int n, double EPSILON, double SCALE, int MAX_IT, double ALPHA,
               double BETA, double GAMMA) {
  // by ACMO
  double ajuste, nureal, interv;

  //
  int vs; /* vertex with smallest value */
  int vh; /* vertex with next smallest value */
  int vg; /* vertex with largest value */

  int i, j, m, row;
  int k;   /* track the number of function evaluations */
  int itr; /* track the number of iterations */

  double **v;    /* holds vertices of simplex */
  double pn, qn; /* values used to create initial simplex */
  double *f;     /* value of function at each vertex */
  double fr;     /* value of function at reflection point */
  double fe;     /* value of function at expansion point */
  double fc;     /* value of function at contraction point */
  double *vr;    /* reflection - coordinates */
  double *ve;    /* expansion - coordinates */
  double *vc;    /* contraction - coordinates */
  double *vm;    /* centroid - coordinates */
  double min;

  double fsum, favg, s, cent;

  /* dynamically allocate arrays */

  /* allocate the rows of the arrays */
  v = (double **)malloc((n + 1) * sizeof(double *));
  f = (double *)malloc((n + 1) * sizeof(double));
  vr = (double *)malloc(n * sizeof(double));
  ve = (double *)malloc(n * sizeof(double));
  vc = (double *)malloc(n * sizeof(double));
  vm = (double *)malloc(n * sizeof(double));

  /* allocate the columns of the arrays */
  for (i = 0; i <= n; i++) {
    v[i] = (double *)malloc(n * sizeof(double));
  }

  /* create the initial simplex */
  /* assume one of the vertices is 0,0 */

  pn = SCALE * (sqrt(n + 1) - 1 + n) / (n * sqrt(2));
  qn = SCALE * (sqrt(n + 1) - 1) / (n * sqrt(2));

  for (i = 0; i < n; i++) {
    v[0][i] = start[i];
  }

  for (i = 1; i <= n; i++) {
    for (j = 0; j < n; j++) {
      if (i - 1 == j) {
        v[i][j] = pn + start[j];
      } else {
        v[i][j] = qn + start[j];
      }
    }
  }
  /* find the initial function values */
  f[0] = fstart;
  for (j = 1; j <= n; j++) {
    f[j] = func(v[j], n);
  }

  k = n + 1;

  /* begin the main loop of the minimization */
  for (itr = 1; itr <= MAX_IT; itr++) {
    /* find the index of the largest value */
    vg = 0;
    for (j = 0; j <= n; j++) {
      if (f[j] > f[vg]) {
        vg = j;
      }
    }

    /* find the index of the smallest value */
    vs = 0;
    for (j = 0; j <= n; j++) {
      if (f[j] < f[vs]) {
        vs = j;
      }
    }

    /* find the index of the second largest value */
    vh = vs;
    for (j = 0; j <= n; j++) {
      if (f[j] > f[vh] && f[j] < f[vg]) {
        vh = j;
      }
    }

    /* calculate the centroid */
    for (j = 0; j <= n - 1; j++) {
      cent = 0.0;
      for (m = 0; m <= n; m++) {
        if (m != vg) {
          cent += v[m][j];
        }
      }
      vm[j] = cent / n;
    }

    /* reflect vg to new vertex vr */
    for (j = 0; j <= n - 1; j++) {
      /*vr[j] = (1+ALPHA)*vm[j] - ALPHA*v[vg][j];*/
      vr[j] = vm[j] + ALPHA * (vm[j] - v[vg][j]);
    }
    fr = func(vr, n);
    k++;

    if (fr < f[vh] && fr >= f[vs]) {
      for (j = 0; j <= n - 1; j++) {
        v[vg][j] = vr[j];
      }
      f[vg] = fr;
    }

    /* investigate a step further in this direction */
    if (fr < f[vs]) {
      for (j = 0; j <= n - 1; j++) {
        /*ve[j] = GAMMA*vr[j] + (1-GAMMA)*vm[j];*/
        ve[j] = vm[j] + GAMMA * (vr[j] - vm[j]);
      }
      fe = func(ve, n);
      k++;

      /* by making fe < fr as opposed to fe < f[vs],
         Rosenbrocks function takes 63 iterations as opposed
         to 64 when using double variables. */

      if (fe < fr) {
        for (j = 0; j <= n - 1; j++) {
          v[vg][j] = ve[j];
        }
        f[vg] = fe;
      } else {
        for (j = 0; j <= n - 1; j++) {
          v[vg][j] = vr[j];
        }
        f[vg] = fr;
      }
    }

    /* check to see if a contraction is necessary */
    if (fr >= f[vh]) {
      if (fr < f[vg] && fr >= f[vh]) {
        /* perform outside contraction */
        for (j = 0; j <= n - 1; j++) {
          /*vc[j] = BETA*v[vg][j] + (1-BETA)*vm[j];*/
          vc[j] = vm[j] + BETA * (vr[j] - vm[j]);
        }
        fc = func(vc, n);
        k++;
      } else {
        /* perform inside contraction */
        for (j = 0; j <= n - 1; j++) {
          /*vc[j] = BETA*v[vg][j] + (1-BETA)*vm[j];*/
          vc[j] = vm[j] - BETA * (vm[j] - v[vg][j]);
        }
        fc = func(vc, n);
        k++;
      }

      if (fc < f[vg]) {
        for (j = 0; j <= n - 1; j++) {
          v[vg][j] = vc[j];
        }
        f[vg] = fc;
      }
      /* at this point the contraction is not successful,
         we must halve the distance from vs to all the
         vertices of the simplex and then continue.
         10/31/97 - modified to account for ALL vertices.
      */
      else {
        for (row = 0; row <= n; row++) {
          if (row != vs) {
            for (j = 0; j <= n - 1; j++) {
              v[row][j] = v[vs][j] + (v[row][j] - v[vs][j]) / 2.0;
            }
          }
        }
        f[vg] = func(v[vg], n);
        k++;
        f[vh] = func(v[vh], n);
        k++;
      }
    }

    /* test for convergence */
    fsum = 0.0;
    for (j = 0; j <= n; j++) {
      fsum += f[j];
    }
    favg = fsum / (n + 1);
    s = 0.0;
    for (j = 0; j <= n; j++) {
      s += pow((f[j] - favg), 2.0) / (n);
    }
    s = sqrt(s);
    if (s < EPSILON)
      break;
  }
  /* end main loop of the minimization */

  /* find the index of the smallest value */
  vs = 0;
  for (j = 0; j <= n; j++) {
    if (f[j] < f[vs]) {
      vs = j;
    }
  }
  for (j = 0; j < n; j++) {
    start[j] = v[vs][j];
    // rebate ponto inviável de volta ao espaço de busca com concentração
    // perto da fronteira tanto maior qto for MENOR o valor de REBATIMENTO
    CorrigeInviavel(&start[j], FuncoesTeste[funcao].inf,
                    FuncoesTeste[funcao].sup);
  }
  min = func(v[vs], n);
  k++;

  for (i = 0; i <= n; i++) {
    free(v[i]);
  }

  free(f);
  free(vr);
  free(ve);
  free(vc);
  free(vm);
  free(v);
  return min;
}


double HookExplore(double (*fobj)(double[], int n), double *xr, double fp,
                   double dx, int n) {
  int i, j;
  double fr;
  double linf, lsup, salvo;

  linf = FuncoesTeste[funcao].inf;
  lsup = FuncoesTeste[funcao].sup;

  for (i = 0; i < n; i++) {
    // first direction
    salvo = xr[i];
    xr[i] = salvo + dx;
    // viability
    CorrigeInviavel(&xr[i], linf, lsup);
    // evaluate
    fr = fobj(xr, n);
    if (fr < fp) {
      // success
      fp = fr;
    } else {
      // failure: other direction
      dx = -dx;
      xr[i] = salvo + dx;
      // viability
      CorrigeInviavel(&xr[i], linf, lsup);
      // evaluate
      fr = fobj(xr, n);
      if (fr < fp) {
        // success
        fp = fr;
      } else {
        // reset direction: ACMO bichado por que houve correção
        xr[i] = salvo;
      }
    }
  }
  return (fp);
}

double HookeJeeves(double (*fobj)(double[], int n), double xc[], double fc,
                   int n, double epsilon, int passos, double scala,
                   double step) {
  double linf, lsup, dx, err, fp, inif;
  static double mdx = 1.0F, melf = 0.0F;
  static int cont = 100;
  int i, m;
  char reduz;

  double *xr = (double *)NULL;
  double *xp = (double *)NULL;

  linf = FuncoesTeste[funcao].inf;
  lsup = FuncoesTeste[funcao].sup;

  xp = (double *)malloc(n * sizeof(double));
  xr = (double *)malloc(n * sizeof(double));
  if (xr == NULL || xp == NULL) {
    fprintf(saida, "ERRO(5): Problemas de memoria!!!");
    fprintf(saida, "ABEND 102");
  }

  inif = fc;
  if (cont > 0) {
    dx = step;
    cont--;
  } else {
    dx = step = mdx;
  }

  m = 0;

  while (m <= passos && FuncaoTeste.numAval < MAXAVA) {
    // Assign base point
    fp = fc;
    memcpy(xr, xc, n * sizeof(double));
    fp = HookExplore(fobj, xr, fp, dx, n);
    // if it doesnt get into; it must be reduced
    reduz = TRUE;
    while (fp < fc && fabs(fp - fc) > epsilon && fabs(fp - SOLUCAO) > epsilon &&
           FuncaoTeste.numAval < MAXAVA) {
      reduz = FALSE;
      // set base point
      fc = fp;
      memcpy(xp, xc, n * sizeof(double));
      memcpy(xc, xr, n * sizeof(double));
      for (i = 0; i < n; i++) {
        xr[i] = xr[i] + (xr[i] - xp[i]);
        CorrigeInviavel(&xr[i], linf, lsup);
      }
      fp = fobj(xr, n);
      fp = HookExplore(fobj, xr, fp, dx, n);
    }
    if (reduz && fabs(fp - SOLUCAO) > epsilon) {
      /*     for (i=0;i<n;i++) {
                   dx[i] = scala * dx[i];
           }
           m++; só incrementa m se houver reduções*/
      dx = scala * dx;
    }
    // difere do original -- sempre incrementa m
    m++;
  }
  if (inif - fc > melf) {
    mdx = step;
    melf = inif - fc;
  }
  free(xr);
  free(xp);
  return (fc);
}