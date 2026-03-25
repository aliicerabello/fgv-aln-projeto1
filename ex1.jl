using LinearAlgebra   # dot()
using Printf          # @sprintf
using Random          # rand()

#------------------------LETRA  A)------------------------

# arrays de arrays (listas de listas em ṕython)
function mat_prod(A::Vector{Vector{Float64}}, B::Vector{Vector{Float64}})
    m = length(A)
    n = length(A[1])
    q = length(B)
    p = length(B[1])

    if n != q
        error("As dimensões não coincidem.")
    end

    # matriz resultado inicializada com zeros
    C = [[0.0 for _ in 1:p] for _ in 1:m]

    for i in 1:m # itera sobre as linhas de A
        for j in 1:p # itera sobre as colunas de B
            cij = 0.0
            for k in 1:n
                cij += A[i][k] * B[k][j]
            end
            C[i][j] = cij
        end
    end

    return C
end


# versão 2 (equivalente a numpy.ndarray)
function mat_prod_np(A::Matrix{Float64}, B::Matrix{Float64})
    m, n  = size(A)
    n2, q = size(B)

    if n != n2
        error("Dimensões incompatíveis.")
    end

    C = zeros(Float64, m, q)

    for i in 1:m
        for j in 1:q
            for k in 1:n
                C[i, j] += A[i, k] * B[k, j]
            end
        end
    end

    return C
end


#------------------------LETRA  B)------------------------


# gerador de array de arrays (equivalente a listas de listas)
function gerar_matriz(m::Int, n::Int)::Vector{Vector{Float64}}
    return [[rand() for _ in 1:n] for _ in 1:m]
end

# gerador de matriz nativa Julia
function gerar_matriz_jl(m::Int, n::Int)::Matrix{Float64}
    return rand(m, n)
end


# equivalente a time.perf_counter
function medir_perf_counter(f, A, B; repeticoes=10)
    tempos = Float64[]
    for _ in 1:repeticoes
        t0 = time_ns()
        f(A, B)
        t1 = time_ns()
        push!(tempos, (t1 - t0) / 1e9)   # converte ns → s
    end
    return sum(tempos) / length(tempos)   # média, igual ao Python
end


# equivalente a time.time
function medir_time(f, A, B; repeticoes=10)
    tempos = Float64[]
    for _ in 1:repeticoes
        t0 = time()
        f(A, B)
        t1 = time()
        push!(tempos, t1 - t0)
    end
    return sum(tempos) / length(tempos)
end


# equivalente a time.process_time 
function medir_process_time(f, A, B; repeticoes=10)
    tempos = Float64[]
    for _ in 1:repeticoes
        t = @elapsed f(A, B)
        push!(tempos, t)
    end
    return sum(tempos) / length(tempos)
end


# equivalente a time.timeit()
function medir_timeit(f, A, B; repeticoes=10, number=3)
    resultados = Float64[]
    for _ in 1:repeticoes
        t = 0.0
        for _ in 1:number
            t += @elapsed f(A, B)
        end
        push!(resultados, t / number)
    end
    return minimum(resultados)
end

# executa e exibe uma "tabela" comparativa entre mat_prod e mat_prod_np
# para diferentes tamanhos de matriz e quatro métodos de medição de tempo similares aos do python
function rodar_testes(tamanhos; repeticoes=10)
    medidores = [
        ("perf_counter", medir_perf_counter),
        ("time.time",    medir_time),
        ("process_time", medir_process_time),
        ("timeit",       medir_timeit),
    ]

    for (m, n, p) in tamanhos
        # gera UMA VEZ e compartilha entre todos os medidores
        A_list = gerar_matriz(m, n)
        B_list = gerar_matriz(n, p)
        A_mat  = Matrix{Float64}(hcat([col for col in eachcol(
                     hcat([A_list[i] for i in 1:m]...)')]...)')   # converte para matriz
        B_mat  = Matrix{Float64}(hcat([col for col in eachcol(
                     hcat([B_list[i] for i in 1:n]...)')]...)')

        # forma mais simples de converter:
        A_mat = Float64[A_list[i][j] for i in 1:m, j in 1:n]
        B_mat = Float64[B_list[i][j] for i in 1:n, j in 1:p]

        # warm-up
        mat_prod(A_list, B_list)
        mat_prod_np(A_mat, B_mat)

        println("\n=== A: $(m)×$(n)  |  B: $(n)×$(p) ===")
        @printf("%-15s %20s %20s\n", "Medidor", "mat_prod (lista)", "mat_prod_np")
        println("-"^57)

        for (nome, medir) in medidores
            t_lista = medir(mat_prod,    A_list, B_list; repeticoes=repeticoes)
            t_np    = medir(mat_prod_np, A_mat,  B_mat;  repeticoes=repeticoes)
            @printf("%-15s %20.6fs %20.6fs\n", nome, t_lista, t_np)
        end
    end
end


#------------------------LETRA  C)------------------------

#produto matricial usando o dot do Julia
function mat_prod_dot(A::Matrix{Float64}, B::Matrix{Float64})
    m, n  = size(A)
    n_B, p = size(B)

    if n != n_B
        error("Dimensões incompatíveis.")
    end

    C = zeros(Float64, m, p)

    for i in 1:m
        for j in 1:p    # substitui o loop k pelo produto escalar nativo
            C[i, j] = dot(A[i, :], B[:, j])
        end
    end

    return C
end


#------------------------LETRA  D)------------------------

#produto matricial nativo do Julia
mat_prod_nativa(A, B) = A * B

# compara toda as implementações usando o medidor equivalente ao perf_counter do Python.
function rodar_testes_native(tamanhos; repeticoes=10)
    for (m, n, p) in tamanhos
        A_list = gerar_matriz(m, n)
        B_list = gerar_matriz(n, p)
        A_mat  = Float64[A_list[i][j] for i in 1:m, j in 1:n]
        B_mat  = Float64[B_list[i][j] for i in 1:n, j in 1:p]

        # aquecimento
        mat_prod(A_list, B_list)
        mat_prod_np(A_mat, B_mat)
        mat_prod_dot(A_mat, B_mat)
        mat_prod_nativa(A_mat, B_mat)

        #mensurar
        t_lista  = medir_perf_counter(mat_prod,        A_list, B_list; repeticoes=repeticoes)
        t_np     = medir_perf_counter(mat_prod_np,     A_mat,  B_mat;  repeticoes=repeticoes)
        t_dot    = medir_perf_counter(mat_prod_dot,    A_mat,  B_mat;  repeticoes=repeticoes)
        t_native = medir_perf_counter(mat_prod_nativa, A_mat,  B_mat;  repeticoes=repeticoes)

        #exibição no terminal
        println("\n=== A: $(m)×$(n)  |  B: $(n)×$(p) ===")
        @printf("%-20s %12s %16s\n", "Função", "Tempo (s)", "Razão vs lista")
        println("-"^50)
        @printf("%-20s %12.6f %16s\n",  "mat_prod (lista)",  t_lista,  "1.00x")
        @printf("%-20s %12.6f %15.2fx\n", "mat_prod_np",     t_np,     t_np/t_lista)
        @printf("%-20s %12.6f %15.2fx\n", "mat_prod_dot",    t_dot,    t_dot/t_lista)
        @printf("%-20s %12.6f %15.2fx\n", "* (nativo)",      t_native, t_native/t_lista)
    end
end



if abspath(PROGRAM_FILE) == @__FILE__

    tamanhos = [
    (5,   5,   5),
    (10,  10,  10),
    (10,  50,  10),
    (20,  100, 20),
    (50,  10,  50),
    (100, 20,  100),
    (50,  50,  50),
    (100, 100, 100),
    (150, 150, 150),
    (200, 200, 200),
    (200, 300, 200),
    (300, 300, 300),
    (500, 300, 500),
    (500, 500, 500),
    ]

    println("=== Aquecimento ===")
    rodar_testes_native([(10, 10, 10)]; repeticoes=1)

    println("\n\n=== Teste 1 ===")
    rodar_testes(tamanhos; repeticoes=10)
    
    println("\n\n=== Teste 2 ===")
    rodar_testes_native(tamanhos; repeticoes=10)


end