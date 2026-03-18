# Graduação em Matemática Aplicada e Ciência de Dados — FGV–EMAp  
**Álgebra Linear Numérica 2026/1**  
Bernardo Freitas Paulo da Costa  
Monitores: Adriel Dias Faria dos Santos e José Thevez Gomes Guedes  

---

# Projeto 1: Complexidade Computacional  
**Álgebra Linear Numérica**  

📅 **Entrega:** 25 de março de 2026  

---

## Instruções

- Justifique seu raciocínio e escreva respostas completas.  
- Os resultados de questões anteriores podem ser usados nas questões seguintes.  
- Explique seu código e comente os gráficos: um gráfico sem referência no texto está “perdido”.  

---

## Questão 1 — Produto de Matrizes

Para esta questão, entregue três arquivos:  
- `ex1.py`  
- `ex1.jl`  
- um relatório em PDF (até 2 páginas) com os resultados dos testes e seus comentários  

#### a) Escreva, tanto em Python como em Julia, uma função `mat_prod(A, B)` que recebe duas matrizes `A` e `B` e retorna o produto `C = AB`, calculando cada entrada `C_ij` como uma soma.

#### b) Teste estas funções com matrizes de tamanhos variados (pequenas e grandes, tanto com `m < n`, como `m > n` e `m = n`) e compare o tempo de execução.   Use apropriadamente as funções de medição de tempo para evitar “erros de medida”.

#### c) Agora, escreva uma função `mat_prod_dot(A, B)` que calcula o produto `C = AB` usando a função de produto escalar (*dot product*) da linguagem para calcular cada entrada `C_ij`.   Como isto afeta o tempo de execução nos testes anteriores?

#### d) Compare com o tempo de execução das funções de produto de matrizes “nativas” da linguagem:  
- `@` em NumPy  
- `*` em Julia  

---

## Questão 2 — Resolvendo Sistemas Tridiagonais

#### a) Escreva, em Python ou Julia, uma função `solve_tridiag(A, b)` que recebe uma matriz quadrada `A` e um vetor `b` e retorna a solução do sistema `Ax = b`.   (Você pode supor que `A` é inversível.)

#### b) Verifique que sua função está correta, fazendo alguns testes.

#### c) Qual é a complexidade computacional da sua função?

#### d) A partir de que tamanho de matriz `A` a função `solve_tridiag` se torna mais rápida do que a função `numpy.linalg.solve` (ou `\` em Julia)?   Como você fez para chegar neste resultado?
