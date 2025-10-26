import random
import numpy as np
import math
def initial_pop(dimension,pop_size):
    population = []
    for _ in range(pop_size):
        individual = [random.uniform(0, 1) for _ in range(dimension)]
        population.append(individual)
    return population

def fitness(individual):
    f1 = individual[0]
    g = 1 + (9/len(individual)-1)*(sum(individual[1:])/len(individual[1:]))
    f2 = g*(1- math.sqrt(f1/g))
    return f1, f2

def mutation(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = random.randint(0,1000)
    return individual

def crossover(parent1,parent2):
    point = random.randint(1,len(parent1)-1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def select_parents(population,num_parents):
    selected = random.choices(population,k=num_parents)
    return selected

def dominationers(population):
    fronts = [[]]
    domination = {}
    
    for i, p in enumerate(population):
        dominadores = []
        for j, q in enumerate(population):
            if i != j:
                f1_p, f2_p = fitness(p)
                f1_q, f2_q = fitness(q)
                # Se p domina q
                if (f1_p <= f1_q and f2_p <= f2_q) and (f1_p < f1_q or f2_p < f2_q):
                    dominadores.append(j)
        
        if not dominadores:
            fronts[0].append(p)
        domination[i] = dominadores

    
    # Processar índices ordenados por quantos cada um domina
    sorted_indices = sorted(domination.items(), key=lambda x: len(x[1]))
    return domination, sorted_indices
def non_dominated_sort(population):

    domination, sorted_indices = dominationers(population)
    fronts = [[]]
    ind_to_idx = {tuple(ind): i for i, ind in enumerate(population)}
    # Criar set dos índices já na primeira frente
    first_front_indices = {ind_to_idx[tuple(ind)] for ind in fronts[0]}

    for idx, dominated_by_idx in sorted_indices:
        # Pular se já está na primeira frente
        if idx in first_front_indices:
            continue
        
        # Tentar colocar em uma frente existente
        placed = False
        for front in fronts:
            # Verificar se é dominado por algum membro da frente
            is_dominated = False
            for member in front:
                member_idx = ind_to_idx[tuple(member)]
                # Verifica se member domina idx
                if idx in domination.get(member_idx, []):
                    is_dominated = True
                    break
            
            if not is_dominated:
                front.append(population[idx])
                placed = True
                break
        
        # Se não coube em nenhuma frente, criar nova
        if not placed:
            fronts.append([population[idx]])

    return fronts, sorted_indices


def genetic_algorithm(dimension, pop_size, num_generations, mutation_rate):
    population = initial_pop(dimension, pop_size)
    
    for generation in range(num_generations):
        # Gerar filhos
        new_population = []
        while len(new_population) < pop_size:
            parents = select_parents(population, 2)
            child1, child2 = crossover(parents[0], parents[1])
            child1 = mutation(child1, mutation_rate)
            child2 = mutation(child2, mutation_rate)
            new_population.extend([child1, child2])
        new_population = new_population[:pop_size]
        
        # Unir pais + filhos
        combined = population + new_population
        
        # Classificar em frentes de Pareto
        fronts, sorted_indices = non_dominated_sort(combined)

        # Selecionar os melhores M indivíduos das frentes
        population = []
        for front in fronts:
            if len(population) + len(front) <= pop_size:
                population.extend(front)
            else:
                # Preencher com indivíduos aleatórios da frente
                remaining = pop_size - len(population)
                population.extend(random.sample(front, remaining))
                break
        
        # Garantir que o melhor está incluído
        best_idx = sorted_indices[0][0]
        best_individual = combined[best_idx]
        if best_individual not in population:
            population[0] = best_individual
    
    # Retornar a primeira frente final
    fronts, _ = non_dominated_sort(population)
    return fronts[0]

# Executar algoritmo
pareto_front = genetic_algorithm(10, 50, 200, 0.01)

print(f"\n=== Frente de Pareto Final ===")
print(f"Total de soluções não-dominadas: {len(pareto_front)}")
print("\nAlgumas soluções da Frente de Pareto:")
for i, ind in enumerate(pareto_front[:5]):
    f1, f2 = fitness(ind)
    print(f"  Solução {i+1}: f1={f1:.4f}, f2={f2:.4f}")


