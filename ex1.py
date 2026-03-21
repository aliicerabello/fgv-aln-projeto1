#------------------------LETRA A)------------------------
import numpy as np

def mat_prod(A:list[list], B:list[list]) -> list[list]: #LISTA DE LISTAS
    m = len(A)          # número de linhas de A
    n = len(A[0])       # número de colunas de A 
    q = len(B)          # número de linhas de B
    p = len(B[0])       # número de colunas de B

    if n != q:
        raise ValueError("As dimensões não coincidem.")
    
    else: 
        # matriz resultado (inicializada com zeros)
        C = [[0 for _ in range(p)] for _ in range(m)]

        for i in range(m):
            for j in range(p): #O(n**3)
                cij = 0
                for k in range(n):
                    cij += A[i][k] * B[k][j]
                C[i][j] = cij #explicar diferença
 
        return C

#fazer o produto usando numpy array

def mat_prod_np(A, B):
    m, n = A.shape
    n2, q = B.shape

    if n != n2:
        raise ValueError("Dimensões incompatíveis")

    C = np.zeros((m, q))

    for i in range(m):
        for j in range(q):
            for k in range(n):
                C[i, j] += A[i, k] * B[k, j]

    return C

# Observação: esta versão usa loops explícitos,
# portanto não aproveita a vetorização do NumPy

    

#------------------------LETRA  B)------------------------

import random
import time
import timeit
import numpy as np

def gerar_matriz(m, n):
    return [[random.random() for _ in range(n)] for _ in range(m)]

def gerar_matriz_np(m, n):
    return np.random.rand(m, n)

def medir_perf_counter(func, A, B, repeticoes=10):
    tempos = []
    for _ in range(repeticoes):
        inicio = time.perf_counter()
        func(A, B)
        fim = time.perf_counter()
        tempos.append(fim - inicio)
    return sum(tempos) / len(tempos)

def medir_time(func, A, B, repeticoes=10):
    tempos = []
    for _ in range(repeticoes):
        inicio = time.time()
        func(A, B)
        fim = time.time()
        tempos.append(fim - inicio)
    return sum(tempos) / len(tempos)

def medir_process_time(func, A, B, repeticoes=10):
    tempos = []
    for _ in range(repeticoes):
        inicio = time.process_time()
        func(A, B)
        fim = time.process_time()
        tempos.append(fim - inicio)
    return sum(tempos) / len(tempos)

def medir_timeit(func, A, B, repeticoes=10):
    timer = timeit.Timer(lambda: func(A, B))
    return min(timer.repeat(repeat=repeticoes, number=3)) / 3

def rodar_testes(tamanhos, repeticoes=10):
    medidores = {
        "perf_counter": medir_perf_counter,
        "time.time":    medir_time,
        "process_time": medir_process_time,
        "timeit":       medir_timeit,
    }

    for (m, n, p) in tamanhos:
        # 1) Gera UMA VEZ e compartilha entre todos os medidores
        A_list = gerar_matriz(m, n)
        B_list = gerar_matriz(n, p)
        A_np   = np.array(A_list)        # 2) converte o MESMO dado para numpy
        B_np   = np.array(B_list)        #    em vez de gerar de novo

        # warm-up (evita custo de inicialização/cache)
        mat_prod(A_list, B_list)
        mat_prod_np(A_np, B_np)

        print(f"\n=== A: {m}×{n}  |  B: {n}×{p} ===")
        print(f"{'Medidor':<15} {'mat_prod (lista)':>20} {'mat_prod_np':>20}")
        print("-" * 57)

        for nome, medir in medidores.items():
            t_lista = medir(mat_prod, A_list, B_list, repeticoes)
            t_np    = medir(mat_prod_np, A_np,   B_np,   repeticoes)
            print(f"{nome:<15} {t_lista:>20.6f}s {t_np:>20.6f}s")

tamanhos = [
    # 🔹 Pequenos (debug + comportamento inicial)
    (5, 5, 5),
    (10, 10, 10),

    # 🔹 Retangulares (m < n)
    (10, 50, 10),
    (20, 100, 20),

    # 🔹 Retangulares (m > n)
    (50, 10, 50),
    (100, 20, 100),

    # 🔹 Quadradas médias
    (50, 50, 50),
    (100, 100, 100),

    # 🔹 Casos maiores (já mostram O(n³))
    (150, 150, 150),
    (200, 200, 200),

    # 🔹 Um caso grande
    (300, 300, 300),
    (500, 300, 500)
]

#rodar_testes(tamanhos, repeticoes=10)

#------------------------LETRA  C)------------------------

def mat_prod_dot(A, B):
    # A e B devem ser np.array para performance
    m, n = A.shape
    n_B, p = B.shape
    
    if n != n_B:
        raise ValueError("Dimensões incompatíveis")
        
    C = np.zeros((m, p))
    
    for i in range(m):
        for j in range(p):
            # Substituímos o loop 'k' pelo produto escalar da 
            # linha i de A com a coluna j de B
            C[i, j] = np.dot(A[i, :], B[:, j])
            
    return C


def rodar_testes_dot(tamanhos, repeticoes=10):
    """
    Compara mat_prod (lista), mat_prod_np (numpy triple loop)
    e mat_prod_dot (numpy com np.dot no laço) nas mesmas dimensões.
    Usa apenas perf_counter — medidor mais confiável.
    """
    for (m, n, p) in tamanhos:
        # mesma matriz para todos — mesmos dados numéricos
        A_list = gerar_matriz(m, n)
        B_list = gerar_matriz(n, p)
        A_np   = np.array(A_list)
        B_np   = np.array(B_list)

        # warm-up
        mat_prod(A_list, B_list)
        mat_prod_np(A_np, B_np)
        mat_prod_dot(A_np, B_np)

        # medição
        t_lista = medir_perf_counter(mat_prod,     A_list, B_list, repeticoes)
        t_np    = medir_perf_counter(mat_prod_np,  A_np,   B_np,   repeticoes)
        t_dot   = medir_perf_counter(mat_prod_dot, A_np,   B_np,   repeticoes)

        print(f"\n=== A: {m}×{n}  |  B: {n}×{p} ===")
        print(f"{'Função':<20} {'Tempo (s)':>12} {'Razão vs lista':>16}")
        print("-" * 50)
        print(f"{'mat_prod (lista)':<20} {t_lista:>12.6f} {'1.00x':>16}")
        print(f"{'mat_prod_np':<20} {t_np:>12.6f} {t_np/t_lista:>15.2f}x")
        print(f"{'mat_prod_dot':<20} {t_dot:>12.6f} {t_dot/t_lista:>15.2f}x")

#rodar_testes_dot(tamanhos, repeticoes=10)

def mat_prod_nativa(A, B):
    return A @ B

def rodar_testes_native(tamanhos, repeticoes=10):
    """
    Compara todas as implementações + operador nativo @
    Usa apenas perf_counter.
    """
    for (m, n, p) in tamanhos:
        A_list = gerar_matriz(m, n)
        B_list = gerar_matriz(n, p)
        A_np   = np.array(A_list)
        B_np   = np.array(B_list)

        # warm-up
        mat_prod(A_list, B_list)
        mat_prod_np(A_np, B_np)
        mat_prod_dot(A_np, B_np)
        mat_prod_nativa(A_np, B_np)

        t_lista  = medir_perf_counter(mat_prod,        A_list, B_list, repeticoes)
        t_np     = medir_perf_counter(mat_prod_np,     A_np,   B_np,   repeticoes)
        t_dot    = medir_perf_counter(mat_prod_dot,    A_np,   B_np,   repeticoes)
        t_native = medir_perf_counter(mat_prod_nativa, A_np,   B_np,   repeticoes)

        print(f"\n=== A: {m}×{n}  |  B: {n}×{p} ===")
        print(f"{'Função':<20} {'Tempo (s)':>12} {'Razão vs lista':>16}")
        print("-" * 50)
        print(f"{'mat_prod (lista)':<20} {t_lista:>12.6f} {'1.00x':>16}")
        print(f"{'mat_prod_np':<20} {t_np:>12.6f} {t_np/t_lista:>15.2f}x")
        print(f"{'mat_prod_dot':<20} {t_dot:>12.6f} {t_dot/t_lista:>15.2f}x")
        print(f"{'@ (nativo)':<20} {t_native:>12.6f} {t_native/t_lista:>15.2f}x")


rodar_testes_native(tamanhos, repeticoes=10)










#fazer o produto usando numpy - OK
#nao contar o tempo da criacao da matriz C de zeros na medicao de tempo - Observação no PDF
#tamanhos = [2, 5, 10, 20, 50, 100, 200, 300, 500] - OK
#fazer 10 casos de cada produto de matriz de tamanhos e calcular a media - OK
#fazer media do tempo do produto de matrizes do mesmo tamanho - OK
#fazer tabela com diferentes medidores de  - OK
