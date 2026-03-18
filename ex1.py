#------------------------LETRA A)------------------------

def mat_prod(A:list[list], B:list[list]) -> list[list]: #LISTA DE LISTAS
    m = len(A)          # número de linhas de A
    n = len(A[0])       # número de colunas de A 
    q = len(B)          # número de linhas de B
    p = len(B[0])       # número de colunas de B

    if n != q:
        return ValueError("As dimensões não coincidem.")
    
    else: 
        # matriz resultado (inicializada com zeros)
        C = [[0 for _ in range(p)] for _ in range(m)]

        for i in range(m):
            for j in range(p): #O(n**3)
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]

        return C


#------------------------LETRA  B)------------------------

import random
import time

def matriz(m,n): #m linhas e n colunas
    return [[random.random() for _ in range(n)] for _ in range(m)]

A = matriz(100)
B = matriz(100)

def tempo_matriz():
    resultados = []

    for i in range(10):
        A = matriz()
        B = matriz()

        inicio = time.perf_counter()
        mat_prod(A, B)
        fim = time.perf_counter()

        resultados.append(fim - inicio)
        media = sum(resultados)/len(resultados)

#fazer media do tempo de matrizes do mesmo tamanho
#fazer tabela com diferentes medidores de tempo
#calcular media e desvio de cada tamanho de matriz pra cada medidor
