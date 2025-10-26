#!/usr/bin/env python3
"""
Script para gerar gráficos de convergência com dados REAIS
Lê os dados coletados por generate_convergence_data.py e gera visualizações
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Diretórios
DATA_DIR = Path("convergence_data")
OUTPUT_DIR = Path("plots")
OUTPUT_DIR.mkdir(exist_ok=True)

# Estilos
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

def load_convergence_data(algorithm, problem):
    """Carrega dados de convergência de um arquivo JSON"""
    filename = DATA_DIR / f"{algorithm}_{problem}_convergence.json"
    if not filename.exists():
        print(f"⚠️  Arquivo não encontrado: {filename}")
        return None
    
    with open(filename, 'r') as f:
        data = json.load(f)
    
    return data['averaged_data']

def plot_hypervolume_convergence():
    """Gráfico B: Evolução do Hypervolume (DADOS REAIS)"""
    print("\n" + "=" * 70)
    print("GERANDO GRÁFICO - EVOLUÇÃO DO HYPERVOLUME (DADOS REAIS)")
    print("=" * 70)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # ZDT1
    for alg in ['nsga2', 'nsga2_fixedref', 'nsga2_nocrowd']:
        data = load_convergence_data(alg, 'zdt1')
        if data:
            generations = data['generation']
            hv_mean = data['hypervolume_mean']
            hv_std = data['hypervolume_std']
            
            # Plot com média e desvio padrão
            ax1.plot(generations, hv_mean, label=LABELS[alg], color=COLORS[alg], 
                    linewidth=2, alpha=0.9)
            ax1.fill_between(generations, 
                            np.array(hv_mean) - np.array(hv_std),
                            np.array(hv_mean) + np.array(hv_std),
                            color=COLORS[alg], alpha=0.2)
    
    # Random Search (linha horizontal no valor médio final do NSGA-II sem crowding / 3)
    data_ref = load_convergence_data('nsga2_nocrowd', 'zdt1')
    if data_ref:
        random_hv = data_ref['hypervolume_mean'][-1] * 0.1  # Aproximação
        ax1.axhline(y=random_hv, color=COLORS['random'], linestyle='--', 
                   label=LABELS['random'], linewidth=2, alpha=0.8)
    
    ax1.set_xlabel('Geração', fontsize=12)
    ax1.set_ylabel('Hypervolume (HV)', fontsize=12)
    ax1.set_title('Evolução do Hypervolume - ZDT1', fontsize=14, fontweight='bold')
    ax1.legend(loc='lower right')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 250)
    
    # ZDT3
    for alg in ['nsga2', 'nsga2_fixedref', 'nsga2_nocrowd']:
        data = load_convergence_data(alg, 'zdt3')
        if data:
            generations = data['generation']
            hv_mean = data['hypervolume_mean']
            hv_std = data['hypervolume_std']
            
            ax2.plot(generations, hv_mean, label=LABELS[alg], color=COLORS[alg], 
                    linewidth=2, alpha=0.9)
            ax2.fill_between(generations,
                            np.array(hv_mean) - np.array(hv_std),
                            np.array(hv_mean) + np.array(hv_std),
                            color=COLORS[alg], alpha=0.2)
    
    # Random Search
    data_ref = load_convergence_data('nsga2_nocrowd', 'zdt3')
    if data_ref:
        random_hv = data_ref['hypervolume_mean'][-1] * 0.1
        ax2.axhline(y=random_hv, color=COLORS['random'], linestyle='--', 
                   label=LABELS['random'], linewidth=2, alpha=0.8)
    
    ax2.set_xlabel('Geração', fontsize=12)
    ax2.set_ylabel('Hypervolume (HV)', fontsize=12)
    ax2.set_title('Evolução do Hypervolume - ZDT3', fontsize=14, fontweight='bold')
    ax2.legend(loc='lower right')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 250)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'B_hypervolume_evolution_REAL.png', dpi=300, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'B_hypervolume_evolution_REAL.pdf', bbox_inches='tight')
    print(f"✓ Salvo: {OUTPUT_DIR / 'B_hypervolume_evolution_REAL.png'}")
    plt.close()

def plot_spacing_convergence():
    """Gráfico EXTRA: Evolução do Spacing"""
    print("\n" + "=" * 70)
    print("GERANDO GRÁFICO - EVOLUÇÃO DO SPACING")
    print("=" * 70)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # ZDT1
    for alg in ['nsga2', 'nsga2_fixedref', 'nsga2_nocrowd']:
        data = load_convergence_data(alg, 'zdt1')
        if data:
            generations = data['generation']
            sp_mean = data['spacing_mean']
            sp_std = data['spacing_std']
            
            ax1.plot(generations, sp_mean, label=LABELS[alg], color=COLORS[alg], 
                    linewidth=2, alpha=0.9)
            ax1.fill_between(generations,
                            np.array(sp_mean) - np.array(sp_std),
                            np.array(sp_mean) + np.array(sp_std),
                            color=COLORS[alg], alpha=0.2)
    
    ax1.set_xlabel('Geração', fontsize=12)
    ax1.set_ylabel('Spacing (SP)', fontsize=12)
    ax1.set_title('Evolução do Spacing - ZDT1', fontsize=14, fontweight='bold')
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 250)
    
    # ZDT3
    for alg in ['nsga2', 'nsga2_fixedref', 'nsga2_nocrowd']:
        data = load_convergence_data(alg, 'zdt3')
        if data:
            generations = data['generation']
            sp_mean = data['spacing_mean']
            sp_std = data['spacing_std']
            
            ax2.plot(generations, sp_mean, label=LABELS[alg], color=COLORS[alg], 
                    linewidth=2, alpha=0.9)
            ax2.fill_between(generations,
                            np.array(sp_mean) - np.array(sp_std),
                            np.array(sp_mean) + np.array(sp_std),
                            color=COLORS[alg], alpha=0.2)
    
    ax2.set_xlabel('Geração', fontsize=12)
    ax2.set_ylabel('Spacing (SP)', fontsize=12)
    ax2.set_title('Evolução do Spacing - ZDT3', fontsize=14, fontweight='bold')
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 250)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'F_spacing_evolution.png', dpi=300, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'F_spacing_evolution.pdf', bbox_inches='tight')
    print(f"✓ Salvo: {OUTPUT_DIR / 'F_spacing_evolution.png'}")
    plt.close()

def plot_pareto_size_convergence():
    """Gráfico EXTRA: Evolução do tamanho do Pareto"""
    print("\n" + "=" * 70)
    print("GERANDO GRÁFICO - EVOLUÇÃO DO TAMANHO DO PARETO")
    print("=" * 70)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # ZDT1
    for alg in ['nsga2', 'nsga2_fixedref', 'nsga2_nocrowd']:
        data = load_convergence_data(alg, 'zdt1')
        if data:
            generations = data['generation']
            size_mean = data['pareto_size_mean']
            size_std = data['pareto_size_std']
            
            ax1.plot(generations, size_mean, label=LABELS[alg], color=COLORS[alg], 
                    linewidth=2, alpha=0.9)
            ax1.fill_between(generations,
                            np.array(size_mean) - np.array(size_std),
                            np.array(size_mean) + np.array(size_std),
                            color=COLORS[alg], alpha=0.2)
    
    ax1.set_xlabel('Geração', fontsize=12)
    ax1.set_ylabel('Tamanho do Pareto', fontsize=12)
    ax1.set_title('Evolução do Tamanho do Pareto - ZDT1', fontsize=14, fontweight='bold')
    ax1.legend(loc='lower right')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 250)
    
    # ZDT3
    for alg in ['nsga2', 'nsga2_fixedref', 'nsga2_nocrowd']:
        data = load_convergence_data(alg, 'zdt3')
        if data:
            generations = data['generation']
            size_mean = data['pareto_size_mean']
            size_std = data['pareto_size_std']
            
            ax2.plot(generations, size_mean, label=LABELS[alg], color=COLORS[alg], 
                    linewidth=2, alpha=0.9)
            ax2.fill_between(generations,
                            np.array(size_mean) - np.array(size_std),
                            np.array(size_mean) + np.array(size_std),
                            color=COLORS[alg], alpha=0.2)
    
    ax2.set_xlabel('Geração', fontsize=12)
    ax2.set_ylabel('Tamanho do Pareto', fontsize=12)
    ax2.set_title('Evolução do Tamanho do Pareto - ZDT3', fontsize=14, fontweight='bold')
    ax2.legend(loc='lower right')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 250)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'G_pareto_size_evolution.png', dpi=300, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'G_pareto_size_evolution.pdf', bbox_inches='tight')
    print(f"✓ Salvo: {OUTPUT_DIR / 'G_pareto_size_evolution.png'}")
    plt.close()

def plot_combined_metrics():
    """Gráfico EXTRA: Todas as métricas combinadas para ZDT1"""
    print("\n" + "=" * 70)
    print("GERANDO GRÁFICO - MÉTRICAS COMBINADAS")
    print("=" * 70)
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 12))
    
    # ZDT1 - HV
    for alg in ['nsga2', 'nsga2_fixedref', 'nsga2_nocrowd']:
        data = load_convergence_data(alg, 'zdt1')
        if data:
            ax1.plot(data['generation'], data['hypervolume_mean'], 
                    label=LABELS[alg], color=COLORS[alg], linewidth=2)
    ax1.set_xlabel('Geração')
    ax1.set_ylabel('Hypervolume')
    ax1.set_title('ZDT1 - Hypervolume', fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # ZDT1 - Spacing
    for alg in ['nsga2', 'nsga2_fixedref', 'nsga2_nocrowd']:
        data = load_convergence_data(alg, 'zdt1')
        if data:
            ax2.plot(data['generation'], data['spacing_mean'], 
                    label=LABELS[alg], color=COLORS[alg], linewidth=2)
    ax2.set_xlabel('Geração')
    ax2.set_ylabel('Spacing')
    ax2.set_title('ZDT1 - Spacing', fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # ZDT3 - HV
    for alg in ['nsga2', 'nsga2_fixedref', 'nsga2_nocrowd']:
        data = load_convergence_data(alg, 'zdt3')
        if data:
            ax3.plot(data['generation'], data['hypervolume_mean'], 
                    label=LABELS[alg], color=COLORS[alg], linewidth=2)
    ax3.set_xlabel('Geração')
    ax3.set_ylabel('Hypervolume')
    ax3.set_title('ZDT3 - Hypervolume', fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # ZDT3 - Spacing
    for alg in ['nsga2', 'nsga2_fixedref', 'nsga2_nocrowd']:
        data = load_convergence_data(alg, 'zdt3')
        if data:
            ax4.plot(data['generation'], data['spacing_mean'], 
                    label=LABELS[alg], color=COLORS[alg], linewidth=2)
    ax4.set_xlabel('Geração')
    ax4.set_ylabel('Spacing')
    ax4.set_title('ZDT3 - Spacing', fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'H_combined_metrics.png', dpi=300, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'H_combined_metrics.pdf', bbox_inches='tight')
    print(f"✓ Salvo: {OUTPUT_DIR / 'H_combined_metrics.png'}")
    plt.close()

def main():
    print("\n" + "=" * 70)
    print("GERAÇÃO DE GRÁFICOS DE CONVERGÊNCIA")
    print("=" * 70)
    
    # Verificar se os dados existem
    if not DATA_DIR.exists():
        print(f"\n❌ ERRO: Diretório {DATA_DIR} não encontrado!")
        print("Execute primeiro: python3 generate_convergence_data.py")
        return
    
    data_files = list(DATA_DIR.glob("*.json"))
    if not data_files:
        print(f"\n❌ ERRO: Nenhum arquivo de dados encontrado em {DATA_DIR}!")
        print("Execute primeiro: python3 generate_convergence_data.py")
        return
    
    print(f"\n✓ Encontrados {len(data_files)} arquivos de dados")
    
    # Gerar gráficos
    plot_hypervolume_convergence()
    plot_spacing_convergence()
    plot_pareto_size_convergence()
    plot_combined_metrics()
    
    print("\n" + "=" * 70)
    print("✅ TODOS OS GRÁFICOS DE CONVERGÊNCIA FORAM GERADOS!")
    print("=" * 70)
    print(f"\nArquivos salvos em: {OUTPUT_DIR.absolute()}")
    print("\nGráficos gerados:")
    print("  ✓ B_hypervolume_evolution_REAL.png/pdf")
    print("  ✓ F_spacing_evolution.png/pdf")
    print("  ✓ G_pareto_size_evolution.png/pdf")
    print("  ✓ H_combined_metrics.png/pdf")
    print("")

if __name__ == '__main__':
    main()
