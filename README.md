# Ocev_MOEA

Implementação de Algoritmo Genético Multi-Objetivo usando o problema de benchmark ZDT1.

## 📋 Descrição

Este projeto implementa um algoritmo evolutivo para otimização multi-objetivo, seguindo os princípios do NSGA-II (Non-dominated Sorting Genetic Algorithm II). O código resolve o problema ZDT1, um benchmark clássico para avaliar algoritmos de otimização multi-objetivo.

## 🎯 Problema ZDT1

O ZDT1 é um problema de minimização com dois objetivos:
- **f1(x) = x₁** - Minimizar a primeira variável
- **f2(x) = g(x) · [1 - √(f1/g)]** - Minimizar a segunda função

Onde:
- `g(x) = 1 + 9 · (soma dos xi de i=2 até n) / (n-1)`
- `n` é o número de variáveis (dimensão = 10)
- `xi` são números inteiros no intervalo [0, 1000]

## 🔧 Estrutura do Código

### Funções Principais

#### `initial_pop(dimension, pop_size)`
Gera uma população inicial aleatória de tamanho M.
- **dimension**: Número de variáveis (genes) em cada indivíduo
- **pop_size**: Tamanho da população (M indivíduos)
- **Retorna**: Lista de indivíduos, onde cada indivíduo é uma lista de inteiros [0, 1000]

#### `fitness(individual)`
Calcula as duas funções objetivo f1 e f2 do problema ZDT1.
- **Entrada**: Um indivíduo (lista de inteiros)
- **Retorna**: Tupla `(f1, f2)` com os valores dos dois objetivos
- As variáveis são normalizadas para [0, 1] dividindo por 1000

#### `mutation(individual, mutation_rate)`
Aplica mutação em um indivíduo.
- **mutation_rate**: Probabilidade de mutação para cada gene
- Para cada posição, com probabilidade `mutation_rate`, o valor é substituído por um novo aleatório [0, 1000]

#### `crossover(parent1, parent2)`
Realiza crossover de um ponto entre dois pais.
- Escolhe um ponto de corte aleatório
- Cria dois filhos combinando os segmentos dos pais
- **Retorna**: Tupla `(child1, child2)` com os dois filhos gerados

#### `select_parents(population, num_parents)`
Seleciona pais aleatoriamente da população.
- Usa seleção aleatória uniforme
- **num_parents**: Número de pais a selecionar (geralmente 2)

#### `non_dominated_sort(population)`
**Função central do NSGA-II**: Classifica a população em frentes de Pareto.

**Algoritmo:**
1. **Primeira frente (F₀)**: Contém todos os indivíduos não-dominados
2. **Frentes subsequentes**: Cada frente Fᵢ contém indivíduos dominados apenas por membros das frentes anteriores

**Conceito de dominância**: Um indivíduo A domina B se:
- A é melhor ou igual em todos os objetivos
- A é estritamente melhor em pelo menos um objetivo

**Otimizações implementadas:**
- Mapeamento `ind_to_idx` para evitar chamadas repetidas a `.index()` (O(n) → O(1))
- Set `first_front_indices` para verificação rápida de pertencimento
- Uso de `.get()` para acessos seguros ao dicionário

#### `genetic_algorithm(dimension, pop_size, num_generations, mutation_rate)`
Executa o loop evolutivo principal.

**Passos por geração:**
1. Avaliar fitness de todos os indivíduos
2. Selecionar pais aleatoriamente
3. Aplicar crossover para gerar filhos
4. Aplicar mutação nos filhos
5. Unir pais e filhos
6. Ordenar por fitness e selecionar os M melhores

**Nota**: Esta função ainda usa ordenação simples, não a classificação por frentes de Pareto. Para implementar NSGA-II completo, deveria usar `non_dominated_sort()`.

## 📊 Parâmetros de Execução

```python
dimension = 10          # Número de variáveis
pop_size = 50          # Tamanho da população (M)
num_generations = 200  # Número de gerações
mutation_rate = 0.01   # Taxa de mutação (1%)
```

## 🚀 Como Executar

```bash
python main.py
```

O programa executa o algoritmo genético e imprime:
- Melhor indivíduo encontrado
- Valores de fitness (f1, f2) do melhor indivíduo

## 📚 Referências

- **ZDT1**: Zitzler, E., Deb, K., & Thiele, L. (2000). Comparison of Multiobjective Evolutionary Algorithms
- **NSGA-II**: Deb, K., et al. (2002). A fast and elitist multiobjective genetic algorithm: NSGA-II

## ⚠️ Melhorias Futuras

1. Integrar `non_dominated_sort()` no loop principal do `genetic_algorithm()`
2. Adicionar plotagem das frentes de Pareto usando matplotlib
3. Implementar crowding distance para melhor diversidade
4. Adicionar visualização das gerações em tempo real

<!-- git remote add origin https://github.com/AmonOnly/Ocev_MOEA.git
git branch -M main
git push -u origin main -->