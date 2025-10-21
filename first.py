import random as rand
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# -------------------------
# Funções de objetivo (suas)
# -------------------------
def f1(x):
    return x / 1000.0

def g(X, N):
    return 1 + 9 * ((np.sum(X) / 1000.0) / (N - 1))

def f2(X, N):
    # X é o indivíduo (array), N = len(X)
    return g(X[1:], N) * (1 - np.sqrt(f1(X[0])))

def evaluate_population(pop):
    """Retorna um array shape (M,2) com (f1,f2) para cada indivíduo da população."""
    M = len(pop)
    vals = np.zeros((M, 2), dtype=float)
    for i, ind in enumerate(pop):
        vals[i, 0] = f1(ind[0])          # f1 depende do primeiro gene
        vals[i, 1] = f2(ind, len(ind))  # f2 depende do indivíduo todo
    return vals

# -------------------------
# Inicialização da população
# -------------------------
def initialpop(Din, M):
    individuos = []
    for _ in range(M):
        individuo = [rand.randint(1, 1000) for _ in range(Din)]
        individuos.append(np.array(individuo, dtype=int))
    return np.array(individuos)

# -------------------------
# Crossover e Mutação
# -------------------------
def one_point_crossover(p1, p2):
    """Crossover por um ponto — retorna dois filhos (copiados)."""
    L = len(p1)
    if L < 2:
        return p1.copy(), p2.copy()
    point = rand.randint(1, L - 1)
    c1 = np.concatenate((p1[:point], p2[point:])).copy()
    c2 = np.concatenate((p2[:point], p1[point:])).copy()
    return c1, c2

def mutation(ind, prob=0.1):
    """Mutação por substituição aleatória com prob por gene."""
    ind = ind.copy()
    for i in range(len(ind)):
        if rand.random() < prob:
            ind[i] = rand.randint(1, 1000)
    return ind

def generate_offspring(pop, M_offspring, crossover_rate=0.9, mut_prob=0.1):
    """Gera M_offspring filhos a partir de 'pop' por torneio simples + crossover + mutação."""
    offspring = []
    pop_size = len(pop)
    while len(offspring) < M_offspring:
        # seleção por torneio simples (tamanho 2)
        i1, i2 = rand.randrange(pop_size), rand.randrange(pop_size)
        p1 = pop[i1] if rand.random() < 0.5 else pop[i2]
        j1, j2 = rand.randrange(pop_size), rand.randrange(pop_size)
        p2 = pop[j1] if rand.random() < 0.5 else pop[j2]

        # crossover
        if rand.random() < crossover_rate:
            c1, c2 = one_point_crossover(p1, p2)
        else:
            c1, c2 = p1.copy(), p2.copy()

        # mutação
        c1 = mutation(c1, prob=mut_prob)
        c2 = mutation(c2, prob=mut_prob)

        offspring.append(c1)
        if len(offspring) < M_offspring:
            offspring.append(c2)

    return np.array(offspring[:M_offspring])

# -------------------------
# Dominância e Non-dominated Sorting
# -------------------------
def dominates(a, b):
    """Retorna True se a domina b (assumimos minimizar ambos os objetivos)."""
    return np.all(a <= b) and np.any(a < b)

def non_dominated_sort(objs):
    """
    objs: array shape (pop_size, n_obj)
    Retorna uma lista de frentes; cada frente é uma lista de índices.
    Implementação O(M^2) (suficiente para tamanhos moderados).
    """
    pop_size = len(objs)
    dominated_count = np.zeros(pop_size, dtype=int)
    dominates_list = [set() for _ in range(pop_size)]
    fronts = []

    # comparar pares
    for p in range(pop_size):
        for q in range(pop_size):
            if p == q:
                continue
            if dominates(objs[p], objs[q]):
                dominates_list[p].add(q)
            elif dominates(objs[q], objs[p]):
                dominated_count[p] += 1

    # primeira frente: indivíduos não dominados
    current_front = [i for i in range(pop_size) if dominated_count[i] == 0]
    fronts.append(current_front)

    # construir frentes subsequentes
    while True:
        next_front = []
        for p in current_front:
            for q in list(dominates_list[p]):
                dominated_count[q] -= 1
                if dominated_count[q] == 0:
                    next_front.append(q)
        if not next_front:
            break
        fronts.append(next_front)
        current_front = next_front

    return fronts

# -------------------------
# Plot helpers
# -------------------------
def plot_fronts(objs, fronts, title='Frentes de Pareto'):
    plt.figure(figsize=(7,5))
    plt.scatter(objs[:,0], objs[:,1], label='População', s=30, alpha=0.6)
    colors = ['red', 'green', 'blue', 'orange', 'purple', 'cyan']
    for i, front in enumerate(fronts):
        pts = objs[front]
        c = colors[i % len(colors)]
        plt.scatter(pts[:,0], pts[:,1], color=c, label=f'Frente {i+1}', edgecolor='k', s=60)
    plt.xlabel('f1 (menor é melhor)')
    plt.ylabel('f2 (menor é melhor)')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_pareto_front_only(objs, fronts, title='Frente de Pareto (Primeira Frente)'):
    """Plota apenas a primeira frente de Pareto."""
    plt.figure(figsize=(7,5))
    first_front = objs[fronts[0]]
    # Ordenar por f1 para conectar os pontos
    sorted_idx = np.argsort(first_front[:, 0])
    sorted_front = first_front[sorted_idx]
    
    plt.plot(sorted_front[:,0], sorted_front[:,1], 'ro-', linewidth=2, markersize=8, label='Frente de Pareto')
    plt.xlabel('f1 (minimizar)')
    plt.ylabel('f2 (minimizar)')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_convergence(history, title='Convergência das Gerações'):
    """Plota a evolução do tamanho da primeira frente ao longo das gerações."""
    plt.figure(figsize=(10,5))
    generations = [h[0] for h in history]
    front1_sizes = [h[1] for h in history]
    
    plt.subplot(1,2,1)
    plt.plot(generations, front1_sizes, 'b-o', linewidth=2, markersize=4)
    plt.xlabel('Geração')
    plt.ylabel('Tamanho da Frente 1')
    plt.title('Evolução da Frente de Pareto')
    plt.grid(True)
    
    # Estatísticas dos objetivos da frente 1
    avg_f1 = [h[2] for h in history]
    avg_f2 = [h[3] for h in history]
    
    plt.subplot(1,2,2)
    plt.plot(generations, avg_f1, 'r-', linewidth=2, label='Média f1')
    plt.plot(generations, avg_f2, 'g-', linewidth=2, label='Média f2')
    plt.xlabel('Geração')
    plt.ylabel('Valor Médio')
    plt.title('Valores Médios na Frente 1')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

def plot_3d_evolution(history_objs, title='Evolução 3D (f1, f2, Geração)'):
    """Mostra a evolução das soluções em 3D."""
    fig = plt.figure(figsize=(10,7))
    ax = fig.add_subplot(111, projection='3d')
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(history_objs)))
    
    for i, (gen, objs) in enumerate(history_objs):
        ax.scatter(objs[:,0], objs[:,1], [gen]*len(objs), 
                  c=[colors[i]], alpha=0.6, s=20)
    
    ax.set_xlabel('f1')
    ax.set_ylabel('f2')
    ax.set_zlabel('Geração')
    ax.set_title(title)
    plt.show()

def plot_diversity(objs, fronts, title='Diversidade das Soluções'):
    """Plota histogramas dos objetivos para analisar diversidade."""
    fig, axes = plt.subplots(2, 2, figsize=(12,10))
    
    # Histograma f1 - toda população
    axes[0,0].hist(objs[:,0], bins=30, color='blue', alpha=0.7, edgecolor='black')
    axes[0,0].set_xlabel('f1')
    axes[0,0].set_ylabel('Frequência')
    axes[0,0].set_title('Distribuição de f1 (toda população)')
    axes[0,0].grid(True, alpha=0.3)
    
    # Histograma f2 - toda população
    axes[0,1].hist(objs[:,1], bins=30, color='green', alpha=0.7, edgecolor='black')
    axes[0,1].set_xlabel('f2')
    axes[0,1].set_ylabel('Frequência')
    axes[0,1].set_title('Distribuição de f2 (toda população)')
    axes[0,1].grid(True, alpha=0.3)
    
    # Histograma f1 - primeira frente
    first_front = objs[fronts[0]]
    axes[1,0].hist(first_front[:,0], bins=20, color='red', alpha=0.7, edgecolor='black')
    axes[1,0].set_xlabel('f1')
    axes[1,0].set_ylabel('Frequência')
    axes[1,0].set_title('Distribuição de f1 (Frente de Pareto)')
    axes[1,0].grid(True, alpha=0.3)
    
    # Histograma f2 - primeira frente
    axes[1,1].hist(first_front[:,1], bins=20, color='orange', alpha=0.7, edgecolor='black')
    axes[1,1].set_xlabel('f2')
    axes[1,1].set_ylabel('Frequência')
    axes[1,1].set_title('Distribuição de f2 (Frente de Pareto)')
    axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def plot_comparison(initial_objs, initial_fronts, final_objs, final_fronts):
    """Compara população inicial vs final."""
    fig, axes = plt.subplots(1, 2, figsize=(14,5))
    
    # População inicial
    axes[0].scatter(initial_objs[:,0], initial_objs[:,1], c='gray', s=30, alpha=0.4, label='População')
    first_front_init = initial_objs[initial_fronts[0]]
    sorted_idx = np.argsort(first_front_init[:, 0])
    sorted_front = first_front_init[sorted_idx]
    axes[0].plot(sorted_front[:,0], sorted_front[:,1], 'ro-', linewidth=2, markersize=8, label='Frente de Pareto')
    axes[0].set_xlabel('f1')
    axes[0].set_ylabel('f2')
    axes[0].set_title('População Inicial')
    axes[0].legend()
    axes[0].grid(True)
    
    # População final
    axes[1].scatter(final_objs[:,0], final_objs[:,1], c='gray', s=30, alpha=0.4, label='População')
    first_front_final = final_objs[final_fronts[0]]
    sorted_idx = np.argsort(first_front_final[:, 0])
    sorted_front = first_front_final[sorted_idx]
    axes[1].plot(sorted_front[:,0], sorted_front[:,1], 'go-', linewidth=2, markersize=8, label='Frente de Pareto')
    axes[1].set_xlabel('f1')
    axes[1].set_ylabel('f2')
    axes[1].set_title('População Final')
    axes[1].legend()
    axes[1].grid(True)
    
    plt.tight_layout()
    plt.show()

# -------------------------
# Exemplo: execução única dos passos solicitados
# -------------------------
if __name__ == '__main__':
    Din = 20     # genes por indivíduo
    M = 200       # tamanho da população (pais)
    M_off = 200  # número de filhos a gerar (pode ser igual a M)
    G = 500  # número de gerações

# População inicial
    pop = initialpop(Din, M)
    initial_objs = evaluate_population(pop)
    initial_fronts = non_dominated_sort(initial_objs)
    
    # Histórico para acompanhar evolução
    history = []
    history_objs = []

    for gen in range(G):
        # Avalia
        objs = evaluate_population(pop)

        # Gera filhos
        offspring = generate_offspring(pop, M_off, crossover_rate=0.9, mut_prob=0.05)
        objs_off = evaluate_population(offspring)

        # Combina
        combined_pop = np.vstack((pop, offspring))
        combined_objs = np.vstack((objs, objs_off))

        # Ordena por dominância
        fronts = non_dominated_sort(combined_objs)

        # Seleciona a nova população
        new_pop = []
        for front in fronts:
            if len(new_pop) + len(front) <= M:
                new_pop.extend(front)
            else:
                faltam = M - len(new_pop)
                # critério de desempate (aleatório simples, ou crowding distance se quiser algo mais NSGA-II)
                chosen = rand.sample(front, faltam)
                new_pop.extend(chosen)
                break

        pop = combined_pop[new_pop]  # nova população

        # Registrar histórico
        if gen % 10 == 0 or gen == G-1:
            current_objs = evaluate_population(pop)
            current_fronts = non_dominated_sort(current_objs)
            front1_objs = current_objs[current_fronts[0]]
            avg_f1 = np.mean(front1_objs[:, 0])
            avg_f2 = np.mean(front1_objs[:, 1])
            history.append((gen, len(current_fronts[0]), avg_f1, avg_f2))
            history_objs.append((gen, front1_objs.copy()))
            print(f"Geração {gen+1}/{G} - Frente 1: {len(current_fronts[0])} indivíduos")

    # Avaliação final
    final_objs = evaluate_population(pop)
    final_fronts = non_dominated_sort(final_objs)

    # Mostrar algumas infos
    print(f'\nPopulação final: {len(pop)} indivíduos')
    for i, f in enumerate(final_fronts):
        print(f'Frente {i+1}: {len(f)} indivíduos')

    # Gráficos
    print("\n--- Gerando gráficos ---")
    
    # 1) Todas as frentes
    plot_fronts(final_objs, final_fronts, title='População Final - Frentes de Dominância')
    
    # 2) Apenas a frente de Pareto
    plot_pareto_front_only(final_objs, final_fronts, title='Frente de Pareto Ótima')
    
    # 3) Convergência ao longo das gerações
    plot_convergence(history, title='Evolução do Algoritmo')
    
    # 4) Comparação inicial vs final
    plot_comparison(initial_objs, initial_fronts, final_objs, final_fronts)
    
    # 5) Diversidade das soluções
    plot_diversity(final_objs, final_fronts, title='Análise de Diversidade')
    
    # 6) Evolução 3D
    plot_3d_evolution(history_objs, title='Evolução da Frente de Pareto em 3D')