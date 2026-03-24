
#------------------------LETRA A)------------------------
def solve_tridiag(A, b):
    """
    Resolve sistema tridiagonal Ax = b usando o método de Thomas.
    A: matriz tridiagonal nxn
    b: vetor do lado direito - tamanho n
    """
    n = len(b)
 
    # Extrai as três diagonais de A
    inf  = [A[i][i-1] for i in range(1, n)]   # sub-diagonal
    diag = [A[i][i]   for i in range(n)]       # diagonal principal
    sup  = [A[i][i+1] for i in range(n-1)]     # super-diagonal
 
    # Criar cópias para não modificar os vetores originais
    sup_prime = [0.0] * (n - 1)
    b_prime   = [0.0] * n
    x         = [0.0] * n
 
 
    # Forward Sweep (fatoração)
    sup_prime[0] = sup[0] / diag[0]
    b_prime[0]   = b[0]  / diag[0]
 
    for i in range(1, n - 1):
        denom        = diag[i] - inf[i-1] * sup_prime[i-1]
        sup_prime[i] = sup[i] / denom
        b_prime[i]   = (b[i] - inf[i-1] * b_prime[i-1]) / denom
 
    b_prime[n-1] = (b[n-1] - inf[n-2] * b_prime[n-2]) / (diag[n-1] - inf[n-2] * sup_prime[n-2])
 
    # Back Substitution (substituição reversa)
    x[n-1] = b_prime[n-1]
 
    for i in range(n - 2, -1, -1):
        x[i] = b_prime[i] - sup_prime[i] * x[i+1]
 
    return x
 


#------------------------LETRA B)------------------------

import time
import random


#medição de tempo das matrizes geradas aleatoriamente usando o perf_counter
def medir_tridiag(func, A, b, repeticoes=10):
    tempos = []
    for _ in range(repeticoes):
        inicio = time.perf_counter() #mensurado com perf_counter
        func(A, b)
        fim = time.perf_counter()
        tempos.append(fim - inicio)
    return sum(tempos) / len(tempos)


"""
Como b é combinação linear das colunas de A, podemos fazer essa combinação e gerar b a partir de um x qualquer. 
Obter esse x é o propósito da função solve_tridiag!
Gerar A e b de forma aleatória não faz sentido no contexto desse problema, por isso criei a função gerar_sistema_tridiag.
"""

def gerar_sistema_tridiag(n):
    # gera x
    x = [random.uniform(1, 5) for _ in range(n)]

    # monta matriz tridiagonal
    A = [[0]*n for _ in range(n)] #só zeros

    for i in range(n):
        A[i][i] = random.uniform(5, 10)  # diagonal dom

        if i > 0:
            A[i][i-1] = random.uniform(1, 3) #diagonal inf

        if i < n-1:
            A[i][i+1] = random.uniform(1, 3) #diagonal sup

    # calcula b = Ax
    b = [0]*n
    for i in range(n):
        for j in range(n):
            b[i] += A[i][j]*x[j]

    return A, b, x



def rodar_teste(tamanhos, repeticoes=10):

    for n in tamanhos:
        A, b, x_real = gerar_sistema_tridiag(n)

        n = len(A[0])
        p = len(b) # p = n

        # x calculado em solve_tridiag
        x_calc = solve_tridiag(A, b)

        #exibir no terminal
        print(f"\n=== A: {n}×{n}  |  b: {p}×{1} ===")
        print(f"{'perf_counter':<15} {'solve_tridiag':>20}")
        print("Calculado:", x_calc)
        print("Esperado :", x_real)
        print("-" * 57)

        #medição
        t_tridiag = medir_tridiag(solve_tridiag, A, b, repeticoes)
        print(f"{t_tridiag:>20.6f}s")

tamanhos = [2, 3, 5, 10, 30, 50, 100, 200, 500, 1000]

#rodar_teste(tamanhos, repeticoes=10)

#------------------------LETRA C)------------------------

import numpy as np


def solve_tridiag_np(A,b):
    return np.linalg.solve(np.array(A), np.array(b))


def rodar_testes(inicio=10, fim=2000, passo=100, repeticoes=10):
    tamanhos, tempos_thomas, tempos_np = [], [], []
    cruzamento = None
    diff_anterior = None
 
    for n in range(inicio, fim + 1, passo):
        A, b, _ = gerar_sistema_tridiag(n)
 
        # aquecimento
        solve_tridiag(A, b)
        solve_tridiag_np(A, b)
 
        t_thomas = medir_tridiag(solve_tridiag, A, b, repeticoes)
        t_np     = medir_tridiag(solve_tridiag_np, A, b, repeticoes)
 
        tamanhos.append(n)
        tempos_thomas.append(t_thomas)
        tempos_np.append(t_np)
 
        # diferença de tempos
        diff = t_np - t_thomas

        # detecta cruzamento (mudança de sinal)
        if diff_anterior is not None:
            if diff_anterior > 0 and diff < 0:
                cruzamento = n

        diff_anterior = diff
 
        print(f"n={n:5d}  thomas={t_thomas:.6f}s  numpy={t_np:.6f}s  "
              f"{'← THOMAS VENCE' if t_thomas < t_np else '← NUMPY VENCE'}")
 
    return tamanhos, tempos_thomas, tempos_np, cruzamento


# rodar
tamanhos, tempos_thomas, tempos_np, cruzamento = rodar_testes(
    10, 2000, 100, repeticoes=10
)

print("\nPonto de cruzamento:", cruzamento)

import matplotlib.pyplot as plt

plt.plot(tamanhos, tempos_thomas, label="Thomas (tridiag)")
plt.plot(tamanhos, tempos_np, label="NumPy solve")
plt.xlabel("Tamanho n")
plt.ylabel("Tempo (s)")
plt.legend()
plt.grid()
plt.show()
