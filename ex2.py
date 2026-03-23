
#------------------------LETRA A)------------------------
"""
resolver usando metodo de thomas
"""
 
 
def solve_tridiag(A, b):
    pass
 

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

        m = len[A]
        n = len[A[0]]
        p = len[b] #verificar em solve_tridiag se o tamanho bate

        # x calculado em solve_tridiag
        x_calc = solve_tridiag(A, b)

        #exibir no terminal
        print(f"\n=== A: {m}×{n}  |  b: {m}×{1} ===")
        print(f"{'perf_counter':<15} {'solve_tridiag':>20}")
        print("Calculado:", x_calc)
        print("Esperado :", x_real)
        print("-" * 57)

        #medição
        t_tridiag = medir_tridiag(solve_tridiag, A, b, repeticoes)
        print(f"{t_tridiag:>20.6f}s")

tamanhos = [2, 3, 5, 10, 30, 50, 100, 200, 500, 1000, 2000]

rodar_teste(tamanhos, repeticoes=10)

#------------------------LETRA C)------------------------

import numpy as np

def solve_tridiag_np(A,b):
    np.linalg.solve(A, b)

def rodar_testes_dot(tamanhos, repeticoes=10):
    """
    compara solve_tridiag_np e solve_tridiag.
    usa só o medidor perf_counter
    """
    A, b, x_real = gerar_sistema_tridiag(n) 

    for _ in tamanhos:
        # mesma matriz para todos (mesmos dados numéricos)
        A, b, x_real = gerar_sistema_tridiag(n)     

        # aquecimento
        solve_tridiag(A,b)
        solve_tridiag_np(A,b)

        # medição
        t_np = medir_tridiag(solve_tridiag_np, A, b, repeticoes)
        t_tridiag = medir_tridiag(solve_tridiag, A, b, repeticoes)
    
        #exibição no terminal
        print(f"\n=== A: {m}×{n}  |  B: {n}×{p} ===")
        print(f"{'Função':<20} {'Tempo (s)':>12} {'Razão vs lista':>16}")
        print("-" * 50)
        print(f"{'mat_prod (lista)':<20} {t_lista:>12.6f} {'1.00x':>16}")
        print(f"{'mat_prod_np':<20} {t_np:>12.6f} {t_np/t_lista:>15.2f}x")
        print(f"{'mat_prod_dot':<20} {t_dot:>12.6f} {t_dot/t_lista:>15.2f}x")

rodar_testes_dot(tamanhos, repeticoes=10)
