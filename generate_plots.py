#!/usr/bin/env python3
"""
Script para gerar todos os gráficos obrigatórios do relatório
Comparação de algoritmos NSGA-II e Random Search em ZDT1 e ZDT3

Gráficos gerados:
A. Fronte de Pareto (ZDT1 e ZDT3)
B. Evolução do Hypervolume
C. Boxplots de Hypervolume
D. Boxplots de Spacing
E. Comparação ZDT1 × ZDT3
"""

import subprocess
import numpy as np
import matplotlib.pyplot as plt
import json
import os
from pathlib import Path

# Configurações
POP_SIZE = 100
GENERATIONS = 250
N_VAR = 50
N_RUNS = 10
REF_POINT_ZDT1 = [1.2, 1.2]
REF_POINT_ZDT3 = [1.2, 1.2]
FIXED_BOUNDS_ZDT1 = [0.0, 1.0, 0.0, 1.0]
FIXED_BOUNDS_ZDT3 = [0.0, 1.0, -1.0, 1.0]

# Criar diretório para salvar gráficos
OUTPUT_DIR = Path("plots")
OUTPUT_DIR.mkdir(exist_ok=True)

# Estilos para os gráficos
plt.style.use('seaborn-v0_8-darkgrid')
COLORS = {
    'nsga2': '#2E86AB',
    'nsga2_fixedref': '#A23B72',
    'nsga2_nocrowd': '#F18F01',
    'random': '#C73E1D'
}

LABELS = {
    'nsga2': 'NSGA-II (padrão)',
    'nsga2_fixedref': 'NSGA-II (fixed bounds)',
    'nsga2_nocrowd': 'NSGA-II (sem crowding)',
    'random': 'Random Search'
}

def run_algorithm(script, problem, extra_args=""):
    """Executa um algoritmo e captura a saída"""
    cmd = f"python3 data/{script} --pop {POP_SIZE} --gen {GENERATIONS} --nvar {N_VAR} --runs {N_RUNS} {extra_args}"
    print(f"Executando: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=".")
    return result.stdout

def parse_pareto_front(output):
    """Extrai o fronte de Pareto da primeira run"""
    lines = output.split('\n')
    pareto = []
    capture = False
    for line in lines:
        if 'Run 1:' in line:
            capture = True
            continue
        if capture:
            if line.strip() == '' or 'HV stats' in line:
                break
            parts = line.split(',')
            if len(parts) == 2:
                try:
                    f1 = float(parts[0].strip())
                    f2 = float(parts[1].strip())
                    pareto.append((f1, f2))
                except:
                    pass
    return np.array(pareto) if pareto else np.array([])

def parse_metrics(output):
    """Extrai HV e Spacing de todas as runs"""
    lines = output.split('\n')
    hv_values = []
    sp_values = []
    
    for line in lines:
        if line.startswith('Run'):
            # Extrai HV e spacing de cada run
            parts = line.split()
            for i, part in enumerate(parts):
                if part.startswith('hv='):
                    hv_values.append(float(part.split('=')[1]))
                if part.startswith('spacing='):
                    sp_values.append(float(part.split('=')[1]))
    
    return hv_values, sp_values

def collect_all_data():
    """Coleta dados de todos os algoritmos"""
    data = {}
    
    # ZDT1
    print("\n" + "="*60)
    print("COLETANDO DADOS - ZDT1")
    print("="*60)
    
    data['zdt1'] = {}
    
    # NSGA-II padrão
    output = run_algorithm('nsga2_zdt1.py', 'zdt1', f'--ref {REF_POINT_ZDT1[0]} {REF_POINT_ZDT1[1]}')
    data['zdt1']['nsga2'] = {
        'pareto': parse_pareto_front(output),
        'hv': parse_metrics(output)[0],
        'sp': parse_metrics(output)[1]
    }
    
    # NSGA-II fixed bounds
    output = run_algorithm('nsga2_zdt1_crowd_fixedref.py', 'zdt1', 
                          f'--ref {REF_POINT_ZDT1[0]} {REF_POINT_ZDT1[1]} --fixed-ref-bounds {" ".join(map(str, FIXED_BOUNDS_ZDT1))}')
    data['zdt1']['nsga2_fixedref'] = {
        'pareto': parse_pareto_front(output),
        'hv': parse_metrics(output)[0],
        'sp': parse_metrics(output)[1]
    }
    
    # NSGA-II sem crowding
    output = run_algorithm('nsga2_zdt1.py', 'zdt1', f'--ref {REF_POINT_ZDT1[0]} {REF_POINT_ZDT1[1]} --no-crowd')
    data['zdt1']['nsga2_nocrowd'] = {
        'pareto': parse_pareto_front(output),
        'hv': parse_metrics(output)[0],
        'sp': parse_metrics(output)[1]
    }
    
    # Random Search
    output = run_algorithm('random_zdt1.py', 'zdt1', f'--ref {REF_POINT_ZDT1[0]} {REF_POINT_ZDT1[1]}')
    data['zdt1']['random'] = {
        'pareto': parse_pareto_front(output),
        'hv': parse_metrics(output)[0],
        'sp': parse_metrics(output)[1]
    }
    
    # ZDT3
    print("\n" + "="*60)
    print("COLETANDO DADOS - ZDT3")
    print("="*60)
    
    data['zdt3'] = {}
    
    # NSGA-II padrão
    output = run_algorithm('nsga2_zdt3.py', 'zdt3', f'--ref {REF_POINT_ZDT3[0]} {REF_POINT_ZDT3[1]}')
    data['zdt3']['nsga2'] = {
        'pareto': parse_pareto_front(output),
        'hv': parse_metrics(output)[0],
        'sp': parse_metrics(output)[1]
    }
    
    # NSGA-II fixed bounds
    output = run_algorithm('nsga2_zdt3_crowd_fixedref.py', 'zdt3', 
                          f'--ref {REF_POINT_ZDT3[0]} {REF_POINT_ZDT3[1]} --fixed-ref-bounds {" ".join(map(str, FIXED_BOUNDS_ZDT3))}')
    data['zdt3']['nsga2_fixedref'] = {
        'pareto': parse_pareto_front(output),
        'hv': parse_metrics(output)[0],
        'sp': parse_metrics(output)[1]
    }
    
    # NSGA-II sem crowding
    output = run_algorithm('nsga2_zdt3.py', 'zdt3', f'--ref {REF_POINT_ZDT3[0]} {REF_POINT_ZDT3[1]} --no-crowd')
    data['zdt3']['nsga2_nocrowd'] = {
        'pareto': parse_pareto_front(output),
        'hv': parse_metrics(output)[0],
        'sp': parse_metrics(output)[1]
    }
    
    # Random Search
    output = run_algorithm('random_zdt3.py', 'zdt3', f'--ref {REF_POINT_ZDT3[0]} {REF_POINT_ZDT3[1]}')
    data['zdt3']['random'] = {
        'pareto': parse_pareto_front(output),
        'hv': parse_metrics(output)[0],
        'sp': parse_metrics(output)[1]
    }
    
    return data

def plot_pareto_fronts(data):
    """A. Gráfico de Fronte de Pareto"""
    print("\n" + "="*60)
    print("GERANDO GRÁFICOS - FRONTE DE PARETO")
    print("="*60)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # ZDT1
    for alg in ['nsga2', 'nsga2_fixedref', 'nsga2_nocrowd', 'random']:
        pareto = data['zdt1'][alg]['pareto']
        if len(pareto) > 0:
            sorted_idx = np.argsort(pareto[:, 0])
            ax1.scatter(pareto[sorted_idx, 0], pareto[sorted_idx, 1], 
                       label=LABELS[alg], color=COLORS[alg], alpha=0.7, s=30)
    
    ax1.set_xlabel('$f_1(x)$', fontsize=12)
    ax1.set_ylabel('$f_2(x)$', fontsize=12)
    ax1.set_title('Fronte de Pareto - ZDT1', fontsize=14, fontweight='bold')
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    
    # ZDT3
    for alg in ['nsga2', 'nsga2_fixedref', 'nsga2_nocrowd', 'random']:
        pareto = data['zdt3'][alg]['pareto']
        if len(pareto) > 0:
            sorted_idx = np.argsort(pareto[:, 0])
            ax2.scatter(pareto[sorted_idx, 0], pareto[sorted_idx, 1], 
                       label=LABELS[alg], color=COLORS[alg], alpha=0.7, s=30)
    
    ax2.set_xlabel('$f_1(x)$', fontsize=12)
    ax2.set_ylabel('$f_2(x)$', fontsize=12)
    ax2.set_title('Fronte de Pareto - ZDT3', fontsize=14, fontweight='bold')
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'A_pareto_fronts.png', dpi=300, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'A_pareto_fronts.pdf', bbox_inches='tight')
    print(f"✓ Salvo: {OUTPUT_DIR / 'A_pareto_fronts.png'}")
    plt.close()

def plot_hypervolume_boxplots(data):
    """C. Boxplots de Hypervolume"""
    print("\n" + "="*60)
    print("GERANDO GRÁFICOS - BOXPLOTS HYPERVOLUME")
    print("="*60)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    algorithms = ['nsga2', 'nsga2_fixedref', 'nsga2_nocrowd', 'random']
    
    # ZDT1
    hv_data_zdt1 = [data['zdt1'][alg]['hv'] for alg in algorithms]
    bp1 = ax1.boxplot(hv_data_zdt1, labels=[LABELS[alg] for alg in algorithms],
                      patch_artist=True, showmeans=True)
    
    for patch, alg in zip(bp1['boxes'], algorithms):
        patch.set_facecolor(COLORS[alg])
        patch.set_alpha(0.7)
    
    ax1.set_ylabel('Hypervolume (HV)', fontsize=12)
    ax1.set_title('Hypervolume - ZDT1', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    ax1.tick_params(axis='x', rotation=15)
    
    # ZDT3
    hv_data_zdt3 = [data['zdt3'][alg]['hv'] for alg in algorithms]
    bp2 = ax2.boxplot(hv_data_zdt3, labels=[LABELS[alg] for alg in algorithms],
                      patch_artist=True, showmeans=True)
    
    for patch, alg in zip(bp2['boxes'], algorithms):
        patch.set_facecolor(COLORS[alg])
        patch.set_alpha(0.7)
    
    ax2.set_ylabel('Hypervolume (HV)', fontsize=12)
    ax2.set_title('Hypervolume - ZDT3', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.tick_params(axis='x', rotation=15)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'C_hypervolume_boxplots.png', dpi=300, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'C_hypervolume_boxplots.pdf', bbox_inches='tight')
    print(f"✓ Salvo: {OUTPUT_DIR / 'C_hypervolume_boxplots.png'}")
    plt.close()

def plot_spacing_boxplots(data):
    """D. Boxplots de Spacing"""
    print("\n" + "="*60)
    print("GERANDO GRÁFICOS - BOXPLOTS SPACING")
    print("="*60)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    algorithms = ['nsga2', 'nsga2_fixedref', 'nsga2_nocrowd', 'random']
    
    # ZDT1
    sp_data_zdt1 = [data['zdt1'][alg]['sp'] for alg in algorithms]
    bp1 = ax1.boxplot(sp_data_zdt1, labels=[LABELS[alg] for alg in algorithms],
                      patch_artist=True, showmeans=True)
    
    for patch, alg in zip(bp1['boxes'], algorithms):
        patch.set_facecolor(COLORS[alg])
        patch.set_alpha(0.7)
    
    ax1.set_ylabel('Spacing (SP)', fontsize=12)
    ax1.set_title('Spacing - ZDT1', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    ax1.tick_params(axis='x', rotation=15)
    
    # ZDT3
    sp_data_zdt3 = [data['zdt3'][alg]['sp'] for alg in algorithms]
    bp2 = ax2.boxplot(sp_data_zdt3, labels=[LABELS[alg] for alg in algorithms],
                      patch_artist=True, showmeans=True)
    
    for patch, alg in zip(bp2['boxes'], algorithms):
        patch.set_facecolor(COLORS[alg])
        patch.set_alpha(0.7)
    
    ax2.set_ylabel('Spacing (SP)', fontsize=12)
    ax2.set_title('Spacing - ZDT3', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.tick_params(axis='x', rotation=15)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'D_spacing_boxplots.png', dpi=300, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'D_spacing_boxplots.pdf', bbox_inches='tight')
    print(f"✓ Salvo: {OUTPUT_DIR / 'D_spacing_boxplots.png'}")
    plt.close()

def plot_comparison_zdt1_vs_zdt3(data):
    """E. Comparação ZDT1 × ZDT3"""
    print("\n" + "="*60)
    print("GERANDO GRÁFICOS - COMPARAÇÃO ZDT1 vs ZDT3")
    print("="*60)
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 12))
    
    algorithms = ['nsga2', 'nsga2_fixedref', 'nsga2_nocrowd', 'random']
    
    # Hypervolume comparison
    hv_zdt1 = [np.mean(data['zdt1'][alg]['hv']) for alg in algorithms]
    hv_zdt3 = [np.mean(data['zdt3'][alg]['hv']) for alg in algorithms]
    
    x = np.arange(len(algorithms))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, hv_zdt1, width, label='ZDT1', alpha=0.8, color='#2E86AB')
    bars2 = ax1.bar(x + width/2, hv_zdt3, width, label='ZDT3', alpha=0.8, color='#A23B72')
    
    ax1.set_ylabel('Hypervolume Médio', fontsize=12)
    ax1.set_title('Comparação de Hypervolume: ZDT1 vs ZDT3', fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels([LABELS[alg] for alg in algorithms], rotation=15, ha='right')
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Spacing comparison
    sp_zdt1 = [np.mean(data['zdt1'][alg]['sp']) for alg in algorithms]
    sp_zdt3 = [np.mean(data['zdt3'][alg]['sp']) for alg in algorithms]
    
    bars3 = ax2.bar(x - width/2, sp_zdt1, width, label='ZDT1', alpha=0.8, color='#2E86AB')
    bars4 = ax2.bar(x + width/2, sp_zdt3, width, label='ZDT3', alpha=0.8, color='#A23B72')
    
    ax2.set_ylabel('Spacing Médio', fontsize=12)
    ax2.set_title('Comparação de Spacing: ZDT1 vs ZDT3', fontsize=14, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels([LABELS[alg] for alg in algorithms], rotation=15, ha='right')
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    
    # HV Boxplot consolidated
    hv_all_data = []
    hv_labels = []
    for alg in algorithms:
        hv_all_data.append(data['zdt1'][alg]['hv'])
        hv_labels.append(f"{LABELS[alg]}\n(ZDT1)")
        hv_all_data.append(data['zdt3'][alg]['hv'])
        hv_labels.append(f"{LABELS[alg]}\n(ZDT3)")
    
    bp3 = ax3.boxplot(hv_all_data, labels=hv_labels, patch_artist=True, showmeans=True)
    
    colors_expanded = []
    for alg in algorithms:
        colors_expanded.append(COLORS[alg])
        colors_expanded.append(COLORS[alg])
    
    for patch, color in zip(bp3['boxes'], colors_expanded):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
    
    ax3.set_ylabel('Hypervolume', fontsize=12)
    ax3.set_title('Distribuição de HV: ZDT1 vs ZDT3', fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3, axis='y')
    ax3.tick_params(axis='x', rotation=45)
    
    # SP Boxplot consolidated
    sp_all_data = []
    sp_labels = []
    for alg in algorithms:
        sp_all_data.append(data['zdt1'][alg]['sp'])
        sp_labels.append(f"{LABELS[alg]}\n(ZDT1)")
        sp_all_data.append(data['zdt3'][alg]['sp'])
        sp_labels.append(f"{LABELS[alg]}\n(ZDT3)")
    
    bp4 = ax4.boxplot(sp_all_data, labels=sp_labels, patch_artist=True, showmeans=True)
    
    for patch, color in zip(bp4['boxes'], colors_expanded):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
    
    ax4.set_ylabel('Spacing', fontsize=12)
    ax4.set_title('Distribuição de Spacing: ZDT1 vs ZDT3', fontsize=14, fontweight='bold')
    ax4.grid(True, alpha=0.3, axis='y')
    ax4.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'E_comparison_zdt1_vs_zdt3.png', dpi=300, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'E_comparison_zdt1_vs_zdt3.pdf', bbox_inches='tight')
    print(f"✓ Salvo: {OUTPUT_DIR / 'E_comparison_zdt1_vs_zdt3.png'}")
    plt.close()

def print_statistics(data):
    """Imprime estatísticas resumidas"""
    print("\n" + "="*60)
    print("ESTATÍSTICAS RESUMIDAS")
    print("="*60)
    
    for problem in ['zdt1', 'zdt3']:
        print(f"\n{problem.upper()}:")
        print("-" * 60)
        for alg in ['nsga2', 'nsga2_fixedref', 'nsga2_nocrowd', 'random']:
            hv = data[problem][alg]['hv']
            sp = data[problem][alg]['sp']
            print(f"\n{LABELS[alg]}:")
            print(f"  HV: min={min(hv):.6f}, mean={np.mean(hv):.6f}, max={max(hv):.6f}, std={np.std(hv):.6f}")
            print(f"  SP: min={min(sp):.6f}, mean={np.mean(sp):.6f}, max={max(sp):.6f}, std={np.std(sp):.6f}")

def main():
    print("\n" + "="*60)
    print("GERAÇÃO DE GRÁFICOS PARA RELATÓRIO")
    print("Algoritmos Evolutivos Multiobjetivo - NSGA-II vs Random Search")
    print("="*60)
    
    # Coletar dados
    data = collect_all_data()
    
    # Gerar gráficos
    plot_pareto_fronts(data)
    plot_hypervolume_boxplots(data)
    plot_spacing_boxplots(data)
    plot_comparison_zdt1_vs_zdt3(data)
    
    # Estatísticas
    print_statistics(data)
    
    print("\n" + "="*60)
    print("TODOS OS GRÁFICOS FORAM GERADOS COM SUCESSO!")
    print(f"Diretório de saída: {OUTPUT_DIR.absolute()}")
    print("="*60)
    print("\nArquivos gerados:")
    print("  ✓ A_pareto_fronts.png/pdf")
    print("  ✓ C_hypervolume_boxplots.png/pdf")
    print("  ✓ D_spacing_boxplots.png/pdf")
    print("  ✓ E_comparison_zdt1_vs_zdt3.png/pdf")
    print("\n")

if __name__ == '__main__':
    main()
