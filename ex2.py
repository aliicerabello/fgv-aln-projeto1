#------------------------LETRA A)------------------------
"""
solve_tridiag(A, b)
===================
Resolve Ax = b quando A é uma matriz tridiagonal invertível,
usando o Método de Thomas (fatoração LU para matrizes tridiagonais).
 
Complexidade: O(n) em tempo e espaço.
"""
 
 
def solve_tridiag(A, b):
    """
    Parâmetros
    ----------
    A : lista de listas (n x n) — matriz tridiagonal invertível
    b : lista de n floats     — vetor do lado direito
 
    Retorna
    -------
    x : lista de n floats — solução de Ax = b
    """
    n = len(b)
 
    # --- Extrai as três diagonais de A ---
    a = [float(A[i][i])     for i in range(n)]          # diagonal principal
    lo = [float(A[i][i-1])  for i in range(1, n)]       # subdiagonal (n-1 elementos)
    up = [float(A[i][i+1])  for i in range(n - 1)]      # superdiagonal (n-1 elementos)
 
    # --- Cópias de trabalho (não altera A nem b) ---
    alpha = list(a)           # diagonal modificada da fatoração
    rhs   = [float(x) for x in b]   # lado direito modificado
 
    # ---------------------------------------------------------------
    # Passo 1 — Forward sweep: fatoração + resolve Ly = b
    #
    #   β_i   = lo[i-1] / α_{i-1}
    #   α_i   = a_i − β_i * up[i-1]
    #   rhs_i = rhs_i − β_i * rhs_{i-1}
    # ---------------------------------------------------------------
    for i in range(1, n):
        beta     = lo[i-1] / alpha[i-1]
        alpha[i] = alpha[i] - beta * up[i-1]
        rhs[i]   = rhs[i]  - beta * rhs[i-1]
 
    # ---------------------------------------------------------------
    # Passo 2 — Back substitution: resolve Ux = y
    #
    #   x_n = rhs_n / α_n
    #   x_i = (rhs_i − up_i * x_{i+1}) / α_i
    # ---------------------------------------------------------------
    x = [0.0] * n
    x[-1] = rhs[-1] / alpha[-1]
 
    for i in range(n - 2, -1, -1):
        x[i] = (rhs[i] - up[i] * x[i+1]) / alpha[i]
 
    return x
 
 

#------------------------LETRA B)------------------------