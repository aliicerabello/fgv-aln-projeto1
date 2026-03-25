#------------------------LETRA A)------------------------
import numpy as np


def mat_prod(A:list[list], B:list[list]) -> list[list]:
    """
    calcula o produto matricial entre duas matrizes A e B.

    parâmetros:
        A (list[list]): matriz de dimensões m x n;
        B (list[list]): matriz de dimensões n x p.

    retorna:
        list[list]: matriz resultante C de dimensões m x p.

    lança:
        ValueError: se o número de colunas de A for diferente do número de linhas de B.

    complexidade:
        O(m * n * p):três laços aninhados sobre as dimensões das matrizes;
                no caso quadrado (m = n = p), i.e., O(n³);

    exemplos:
        >>> A = [[1, 2], [3, 4]]
        >>> B = [[5, 6], [7, 8]]
        >>> mat_prod(A, B)
        [[19, 22], [43, 50]]

        >>> mat_prod([[1, 2, 3]], [[4], [5], [6]])
        [[32]]
    """

    m = len(A)          # número de linhas de A
    n = len(A[0])       # número de colunas de A 
    n_B = len(B)          # número de linhas de B
    p = len(B[0])       # número de colunas de B

    if n != n_B:
        raise ValueError("As dimensões não coincidem.")
    
    else: 
        C = [[0 for _ in range(p)] for _ in range(m)] # matriz (m x p) resultado (inicializada com zeros)

        for i in range(m): # itera sobre as linhas de A
            for j in range(p): #itera sobre as colunas de B
                cij = 0
                for k in range(n):
                    cij += A[i][k] * B[k][j]
                C[i][j] = cij
            # atribuição fora do laço interno: acumula primeiro em cij e só
            # depois escreve em C[i][j], o que evita acessos repetidos à lista
        return C



def mat_prod_np(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """
    calcula o produto matricial entre dois arrays NumPy A e B.

    parâmetros:
        A (np.ndarray): matriz de dimensões m x n;
        B (np.ndarray): matriz de dimensões n x q.

    retorna:
        np.ndarray: matriz resultado C de dimensões m x q (dtype float64).

    lança:
        ValueError: se o número de colunas de A for diferente do número de linhas de B.

    complexidade:
        Tempo:  O(m * n * q): três laços aninhados;

    exemplos:
        >>> import numpy as np
        >>> A = np.array([[1, 2], [3, 4]])
        >>> B = np.array([[5, 6], [7, 8]])
        >>> mat_prod_np(A, B)
        array([[19., 22.],
               [43., 50.]])
    """
    m, n = A.shape
    n2, q = B.shape

    if n != n2:
        raise ValueError("Dimensões incompatíveis")

    C = np.zeros((m, q)) # matriz resultado inicializada com zeros

    for i in range(m): #itera sobre as linhas de A
        for j in range(q): #itera sobre as colunas de B
            for k in range(n):
                C[i, j] += A[i, k] * B[k, j] # produto interno entre a linha i de A e a coluna j de B

    return C

# OBS: essa função usa loops explícitos, i.e., não aproveita a vetorização do numpy


#------------------------LETRA  B)------------------------

import random
import time
import timeit
import numpy as np

def gerar_matriz(m:int, n:int) -> list[list[float]]:
    """
    gera uma matriz m x n preenchida com valores aleatórios entre 0 e 1.

    parâmetros:
        m (int): número de linhas da matriz;
        n (int): número de colunas da matriz.

    retorna:
        list[list[float]]: matriz representada como lista de listas de floats.

    exemplos:
        >>> gerar_matriz(2, 3)
        [[0.844, 0.758, 0.421], [0.259, 0.511, 0.405]] 
    """

    return [[random.random() for _ in range(n)] for _ in range(m)]


def gerar_matriz_np(m:int, n:int) -> np.ndarray:
    """
    gera uma matriz NumPy m x n preenchida com valores aleatórios entre 0 e 1.

    parâmetros:
        m (int): número de linhas da matriz.
        n (int): número de colunas da matriz.

    retorna:
        np.ndarray: array de dimensões m x n com dtype float64.

    exemplos:
        >>> np.random.seed(0)
        >>> gerar_matriz_np(2, 3)
        array([[0.549, 0.715, 0.603],
               [0.545, 0.424, 0.646]])
    """

    return np.random.rand(m, n)


def medir_perf_counter(func, A, B, repeticoes=10) -> float:
    """
    mede o tempo médio de execução de func(A, B) usando time.perf_counter().

    parâmetros:
        func (callable): função a ser medida; deve aceitar dois argumentos (A, B);
        A: primeiro argumento passado a func;
        B: segundo argumento passado a func;
        repeticoes (int): número de execuções para calcular a média (padrão: 10).

    retorna:
        float: tempo médio de execução em segundos.
    """

    tempos = []
    for _ in range(repeticoes):
        inicio = time.perf_counter()
        func(A, B)
        fim = time.perf_counter()
        tempos.append(fim - inicio)
    return sum(tempos) / len(tempos)


def medir_time(func, A, B, repeticoes=10) -> float:
    """
    mede o tempo médio de execução de func(A, B) usando time.time().

    parâmetros:
        func (callable): função a ser medida; deve aceitar dois argumentos (A, B);
        A: primeiro argumento passado a func;
        B: segundo argumento passado a func;
        repeticoes (int): número de execuções para calcular a média (padrão: 10).

    retorna:
        float: tempo médio de execução em segundos.
    """

    tempos = []
    for _ in range(repeticoes):
        inicio = time.time()
        func(A, B)
        fim = time.time()
        tempos.append(fim - inicio)
    return sum(tempos) / len(tempos)


def medir_process_time(func, A, B, repeticoes=10) -> float:
    """
    mede o tempo médio de execução de func(A, B) usando time.process_time().

    parâmetros:
        func (callable): função a ser medida; deve aceitar dois argumentos (A, B);
        A: primeiro argumento passado a func;
        B: segundo argumento passado a func;
        repeticoes (int): número de execuções para calcular a média (padrão: 10).

    retorna:
        float: tempo médio de execução em segundos.
    """
    tempos = []
    for _ in range(repeticoes):
        inicio = time.process_time()
        func(A, B)
        fim = time.process_time()
        tempos.append(fim - inicio)
    return sum(tempos) / len(tempos)


def medir_timeit(func, A, B, repeticoes=10) -> float:
    """
    mede o tempo médio de execução de func(A, B) usando timeit.Timer;

    usa timer.repeat() com number=3 execuções por rodada e retorna a média 
    da rodada mais rápida (min sobre as repetições).

    parâmetros:
        func (callable): função a ser medida; deve aceitar dois argumentos (A, B).
        A: primeiro argumento passado a func (ex: matriz).
        B: segundo argumento passado a func (ex: matriz).
        repeticoes (int): número de rodadas para timer.repeat() (padrão: 10).

    retorna:
        float: média do tempo por execução na rodada mais rápida (em segundos).
    """
    timer = timeit.Timer(lambda: func(A, B))
    return min(timer.repeat(repeat=repeticoes, number=3)) / 3

def rodar_testes(tamanhos, repeticoes=10):
    """
    Executa e exibe uma "tabela" comparativa entre mat_prod e mat_prod_np
    para diferentes tamanhos de matriz e quatro métodos de medição de tempo.

    parâmetros:
        tamanhos (list[tuple[int, int, int]]): lista de triplas (m, n, p), onde
            m = linhas de A, n = colunas de A / linhas de B, p = colunas de B.
        repeticoes (int): número de repetições passado a cada função de medição.
            (padrão: 10).

    retorna:
        None (os resultados são impressos diretamente no terminal).

    saída esperada (exemplo para tamanhos=[(2, 2, 2)]):
        === A: 2x2  |  B: 2x2 ===
        Medidor           mat_prod (lista)          mat_prod_np
        ---------------------------------------------------------
        perf_counter              0.000012s            0.000034s
        time.time                 0.000011s            0.000033s
        process_time              0.000010s            0.000031s
        timeit                    0.000009s            0.000030s
    """

    medidores = {
        "perf_counter": medir_perf_counter,
        "time.time":    medir_time,
        "process_time": medir_process_time,
        "timeit":       medir_timeit,
    }

    for (m, n, p) in tamanhos:
        # gera a matriz uma  só vez e compartilha entre todos os medidores
        A_list = gerar_matriz(m, n)
        B_list = gerar_matriz(n, p)
        A_np   = np.array(A_list)        #    converte a mesma matriz pra numpy
        B_np   = np.array(B_list)        #    em vez de gerar outra matriz

        # aquecimento
        mat_prod(A_list, B_list)
        mat_prod_np(A_np, B_np)

        # exibir no terminal
        print(f"\n=== A: {m}×{n}  |  B: {n}×{p} ===")
        print(f"{'Medidor':<15} {'mat_prod (lista)':>20} {'mat_prod_np':>20}")
        print("-" * 57)

        # medição
        for nome, medir in medidores.items():
            t_lista = medir(mat_prod, A_list, B_list, repeticoes)
            t_np    = medir(mat_prod_np, A_np,   B_np,   repeticoes)
            print(f"{nome:<15} {t_lista:>20.6f}s {t_np:>20.6f}s")


#------------------------LETRA  C)------------------------

def mat_prod_dot(A:np.ndarray, B:np.ndarray) -> np.ndarray:
    """
    calcula o produto matricial A x B substituindo o laço interno pelo
    produto escalar nativo np.dot().

    parâmetros:
        A (np.ndarray): matriz de dimensões m x n;
        B (np.ndarray): matriz de dimensões n x p.

    retorna:
        np.ndarray: matriz resultado C de dimensões m x p, dtype float64.

    lança:
        ValueError: se o número de colunas de A for diferente do número de linhas de B.

    complexidade:
        tempo:  O(m * n * p) — mesma complexidade que as versões anteriores, mas 
        o laço mais interno (k) roda em C via NumPy.

    exemplos:
        >>> A = np.array([[1, 2], [3, 4]])
        >>> B = np.array([[5, 6], [7, 8]])
        >>> mat_prod_dot(A, B)
        array([[19., 22.],
               [43., 50.]])
    """
        
    m, n = A.shape
    n_B, p = B.shape     # A e B devem ser np.array

    if n != n_B:
        raise ValueError("Dimensões incompatíveis")
        
    C = np.zeros((m, p))  # matriz (m x p) resultado (inicializada com zeros)
    
    for i in range(m):  # itera sobre as linhas de A
        for j in range(p):  # itera sobre as colunas de B
            C[i, j] = np.dot(A[i, :], B[:, j])
            # np.dot: substitui o laço k das versões anteriores
            
    return C

#------------------------LETRA  D)------------------------


def mat_prod_nativa(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """
    calcula o produto matricial A x B usando o operador nativo @ do NumPy.

    parâmetros:
        A (np.ndarray): matriz de dimensões m x n;
        B (np.ndarray): matriz de dimensões n x p.

    retorna:
        np.ndarray: matriz resultado de dimensões m x p.

    lança:
        ValueError: levantado pelo NumPy se as dimensões
            forem incompatíveis.

    complexidade:
        tempo:  O(m * n * p) no pior caso, mas constantes otimizadas;

    exemplos:
        >>> A = np.array([[1, 2], [3, 4]])
        >>> B = np.array([[5, 6], [7, 8]])
        >>> mat_prod_nativa(A, B)
        array([[19, 22],
               [43, 50]])
    """

    return A @ B

def rodar_testes_comparar(tamanhos:list[tuple[int, int, int]], repeticoes: int = 10) -> None:
    """
    compara o desempenho das quatro implementações usando perf_counter como medidor.

    para cada combinação de dimensões (m, n, p), mede o tempo médio de
    mat_prod, mat_prod_np, mat_prod_dot e mat_prod_nativa, exibindo os
    resultados em tabela com a razão de tempo de cada implementação em
    relação à mat_prod com listas Python.

    parâmetros:
        tamanhos (list[tuple[int, int, int]]): lista de triplas (m, n, p), onde
            m = linhas de A, n = colunas de A / linhas de B, p = colunas de B.
        repeticoes (int): número de repetições passado a medir_perf_counter.
            (padrão: 10).

    retorna:
        None: os resultados são impressos diretamente no terminal.

    saída esperada (exemplo para tamanhos=[(2, 2, 2)]):
        === A: 2x2  |  B: 2x2 ===
        Função                  Tempo (s)     Razão vs lista
        --------------------------------------------------
        mat_prod (lista)         0.000012           1.00x
        mat_prod_np              0.000034           2.83x
        mat_prod_dot             0.000021           1.75x
        @ (nativo)               0.000001           0.08x
    """

    for (m, n, p) in tamanhos:
        A_list = gerar_matriz(m, n)
        B_list = gerar_matriz(n, p)
        A_np   = np.array(A_list)
        B_np   = np.array(B_list)

        # aquecimento
        mat_prod(A_list, B_list)
        mat_prod_np(A_np, B_np)
        mat_prod_dot(A_np, B_np)
        mat_prod_nativa(A_np, B_np)

        # medição
        t_lista  = medir_perf_counter(mat_prod,        A_list, B_list, repeticoes)
        t_np     = medir_perf_counter(mat_prod_np,     A_np,   B_np,   repeticoes)
        t_dot    = medir_perf_counter(mat_prod_dot,    A_np,   B_np,   repeticoes)
        t_native = medir_perf_counter(mat_prod_nativa, A_np,   B_np,   repeticoes)
        razao_np = t_np/t_lista                     
        razao_dot = t_dot/t_lista         
        razao_native = t_native/t_lista        

        # exibição no terminal 
        print(f"\n=== A: {m}×{n}  |  B: {n}×{p} ===")
        print(f"{'Função':<20} {'Tempo (s)':>12} {'Razão vs lista':>16}")
        print("-" * 50)
        print(f"{'mat_prod (lista)':<20} {t_lista:>12.6f} {'1.00x':>16}")
        print(f"{'mat_prod_np':<20} {t_np:>12.6f} {razao_np:>15.2f}x")
        print(f"{'mat_prod_dot':<20} {t_dot:>12.6f} {razao_dot:>15.2f}x")
        print(f"{'@ (nativo)':<20} {t_native:>12.6f} {razao_native:>15.2f}x")



#------------------------TESTES------------------------

# TEMPO QUE MEU COMPUTADOR COMPILOU = 10min29s51ms;
# Seguindo as orientações do teste rápido demorar até 10min, 
# optei por não calcular 10 repetições em matrizes maiores, e sim apenas 2.

if __name__ == "__main__":

    tamanhos = [
        (10,  10,  10),
        (10,  50,  10),
        (20,  100, 20),
        (50,  10,  50),
        (50,  50,  50),
        (100, 50,  100),
        (100, 100, 100),
    ]

    tamanhos_grande = [
        (100,  150,  100),
        (150, 150, 150),
        (200,  200, 200),
    ]

    print("\n\n=== Teste 1 ===")
    
    rodar_testes(tamanhos, repeticoes=10)
    rodar_testes(tamanhos_grande, repeticoes=2)

    print("\n\n=== Teste 2 ===")

    rodar_testes_comparar(tamanhos, repeticoes=10)
    rodar_testes_comparar(tamanhos_grande, repeticoes=2)
