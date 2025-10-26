#!/usr/bin/env python3
"""
Script para coletar dados de convergência (Hypervolume, Spacing, tamanho do Pareto)
ao longo das gerações para todos os algoritmos NSGA-II

Este script executa os algoritmos com track_convergence=True e salva os dados.
"""

import sys
sys.path.insert(0, 'data')

import json
import numpy as np
from pathlib import Path

# Importar os algoritmos
from nsga2_zdt1 import nsga2 as nsga2_zdt1_func, hypervolume, spacing
from nsga2_zdt3 import nsga2 as nsga2_zdt3_func

# Configurações
POP_SIZE = 100
GENERATIONS = 250
N_VAR = 50
N_RUNS = 3  # Menos runs para convergência (mais rápido)
REF_POINT_ZDT1 = (1.2, 1.2)
REF_POINT_ZDT3 = (1.2, 1.2)
FIXED_BOUNDS_ZDT1 = ((0.0, 1.0), (0.0, 1.0))
FIXED_BOUNDS_ZDT3 = ((0.0, 1.0), (-1.0, 1.0))

# Diretório de saída
OUTPUT_DIR = Path("convergence_data")
OUTPUT_DIR.mkdir(exist_ok=True)

print("=" * 70)
print("COLETANDO DADOS DE CONVERGÊNCIA")
print("=" * 70)
print(f"População: {POP_SIZE}, Gerações: {GENERATIONS}, Variáveis: {N_VAR}")
print(f"Execuções: {N_RUNS}")
print("")

def collect_convergence(problem, algorithm_name, nsga2_func, ref_point, fixed_bounds=None, no_crowding=False):
    """Coleta dados de convergência para um algoritmo específico"""
    print(f"\nColetando: {algorithm_name} - {problem.upper()}")
    print("-" * 70)
    
    all_runs_data = []
    
    for run in range(N_RUNS):
        print(f"  Run {run + 1}/{N_RUNS}...", end=" ", flush=True)
        
        result = nsga2_func(
            problem=problem,
            pop_size=POP_SIZE,
            n_var=N_VAR,
            generations=GENERATIONS,
            p_crossover=0.9,
            p_mut=0.05,
            alpha=0.5,
            fixed_bounds=fixed_bounds,
            no_crowding=no_crowding,
            ref_point=ref_point,
            track_convergence=True
        )
        
        pareto, evals, convergence_data = result
        all_runs_data.append(convergence_data)
        
        print(f"✓ (Pareto final: {len(pareto)} soluções)")
    
    # Calcular médias e desvios padrão ao longo das gerações
    avg_data = {
        'generation': convergence_data['generation'],  # Mesma para todas as runs
        'hypervolume_mean': [],
        'hypervolume_std': [],
        'spacing_mean': [],
        'spacing_std': [],
        'pareto_size_mean': [],
        'pareto_size_std': []
    }
    
    n_gens = len(convergence_data['generation'])
    for gen_idx in range(n_gens):
        hvs = [run_data['hypervolume'][gen_idx] for run_data in all_runs_data]
        sps = [run_data['spacing'][gen_idx] for run_data in all_runs_data]
        sizes = [run_data['pareto_size'][gen_idx] for run_data in all_runs_data]
        
        avg_data['hypervolume_mean'].append(np.mean(hvs))
        avg_data['hypervolume_std'].append(np.std(hvs))
        avg_data['spacing_mean'].append(np.mean(sps))
        avg_data['spacing_std'].append(np.std(sps))
        avg_data['pareto_size_mean'].append(np.mean(sizes))
        avg_data['pareto_size_std'].append(np.std(sizes))
    
    # Salvar dados
    filename = OUTPUT_DIR / f"{algorithm_name}_{problem}_convergence.json"
    with open(filename, 'w') as f:
        json.dump({
            'config': {
                'algorithm': algorithm_name,
                'problem': problem,
                'pop_size': POP_SIZE,
                'generations': GENERATIONS,
                'n_var': N_VAR,
                'n_runs': N_RUNS,
                'ref_point': ref_point
            },
            'averaged_data': avg_data,
            'all_runs': all_runs_data
        }, f, indent=2)
    
    print(f"  ✓ Dados salvos: {filename}")
    
    return avg_data

# Coletar dados para ZDT1
print("\n" + "=" * 70)
print("ZDT1")
print("=" * 70)

zdt1_nsga2 = collect_convergence(
    'zdt1', 'nsga2', nsga2_zdt1_func, REF_POINT_ZDT1
)

zdt1_nsga2_fixedref = collect_convergence(
    'zdt1', 'nsga2_fixedref', nsga2_zdt1_func, REF_POINT_ZDT1, 
    fixed_bounds=FIXED_BOUNDS_ZDT1
)

zdt1_nsga2_nocrowd = collect_convergence(
    'zdt1', 'nsga2_nocrowd', nsga2_zdt1_func, REF_POINT_ZDT1,
    no_crowding=True
)

# Coletar dados para ZDT3
print("\n" + "=" * 70)
print("ZDT3")
print("=" * 70)

zdt3_nsga2 = collect_convergence(
    'zdt3', 'nsga2', nsga2_zdt3_func, REF_POINT_ZDT3
)

zdt3_nsga2_fixedref = collect_convergence(
    'zdt3', 'nsga2_fixedref', nsga2_zdt3_func, REF_POINT_ZDT3,
    fixed_bounds=FIXED_BOUNDS_ZDT3
)

zdt3_nsga2_nocrowd = collect_convergence(
    'zdt3', 'nsga2_nocrowd', nsga2_zdt3_func, REF_POINT_ZDT3,
    no_crowding=True
)

print("\n" + "=" * 70)
print("✅ COLETA DE DADOS CONCLUÍDA")
print("=" * 70)
print(f"\nArquivos salvos em: {OUTPUT_DIR.absolute()}")
print("\nPróximo passo: Execute 'python3 plot_convergence.py' para gerar gráficos")
print("")
