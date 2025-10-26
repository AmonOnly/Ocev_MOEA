#!/usr/bin/env python3
"""
Script para gerar gráfico B: Evolução do Hypervolume ao longo das gerações

Este script requer uma versão modificada dos algoritmos que salva HV a cada geração.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Configurações
OUTPUT_DIR = Path("plots")
OUTPUT_DIR.mkdir(exist_ok=True)

# Estilos
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

def generate_synthetic_evolution_data(final_hv, n_generations=250, algorithm='nsga2'):
    """
    Gera dados sintéticos de evolução baseado no HV final
    (Para demonstração - idealmente seria coletado durante execução)
    """
    generations = np.arange(0, n_generations + 1)
    
    if algorithm == 'random':
        # Random search não evolui - constante
        hv_evolution = np.full(len(generations), final_hv)
    elif algorithm == 'nsga2_nocrowd':
        # Convergência mais lenta e instável
        hv_evolution = final_hv * (1 - np.exp(-generations / 80)) * (0.95 + 0.05 * np.random.randn(len(generations)) * 0.1)
    else:
        # NSGA-II: convergência rápida e estável
        if algorithm == 'nsga2':
            rate = 50
        else:  # fixedref
            rate = 60
        hv_evolution = final_hv * (1 - np.exp(-generations / rate))
        # Adiciona pequeno ruído
        hv_evolution += np.random.randn(len(generations)) * final_hv * 0.02
        hv_evolution = np.clip(hv_evolution, 0, final_hv * 1.1)
    
    return generations, hv_evolution

def plot_hypervolume_evolution():
    """B. Gráfico de Evolução do Hypervolume"""
    print("\n" + "="*60)
    print("GERANDO GRÁFICO - EVOLUÇÃO DO HYPERVOLUME")
    print("="*60)
    
    # Valores finais aproximados (baseado em execuções típicas)
    # Estes valores devem ser substituídos por dados reais de execuções
    final_hvs_zdt1 = {
        'nsga2': 0.65,
        'nsga2_fixedref': 0.63,
        'nsga2_nocrowd': 0.58,
        'random': 0.35
    }
    
    final_hvs_zdt3 = {
        'nsga2': 0.50,
        'nsga2_fixedref': 0.48,
        'nsga2_nocrowd': 0.43,
        'random': 0.25
    }
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # ZDT1
    for alg in ['nsga2', 'nsga2_fixedref', 'nsga2_nocrowd', 'random']:
        gen, hv = generate_synthetic_evolution_data(final_hvs_zdt1[alg], algorithm=alg)
        
        if alg == 'random':
            ax1.axhline(y=hv[0], color=COLORS[alg], linestyle='--', 
                       label=LABELS[alg], linewidth=2, alpha=0.8)
        else:
            ax1.plot(gen, hv, label=LABELS[alg], color=COLORS[alg], 
                    linewidth=2, alpha=0.8)
    
    ax1.set_xlabel('Geração', fontsize=12)
    ax1.set_ylabel('Hypervolume (HV)', fontsize=12)
    ax1.set_title('Evolução do Hypervolume - ZDT1', fontsize=14, fontweight='bold')
    ax1.legend(loc='lower right')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 250)
    
    # ZDT3
    for alg in ['nsga2', 'nsga2_fixedref', 'nsga2_nocrowd', 'random']:
        gen, hv = generate_synthetic_evolution_data(final_hvs_zdt3[alg], algorithm=alg)
        
        if alg == 'random':
            ax2.axhline(y=hv[0], color=COLORS[alg], linestyle='--', 
                       label=LABELS[alg], linewidth=2, alpha=0.8)
        else:
            ax2.plot(gen, hv, label=LABELS[alg], color=COLORS[alg], 
                    linewidth=2, alpha=0.8)
    
    ax2.set_xlabel('Geração', fontsize=12)
    ax2.set_ylabel('Hypervolume (HV)', fontsize=12)
    ax2.set_title('Evolução do Hypervolume - ZDT3', fontsize=14, fontweight='bold')
    ax2.legend(loc='lower right')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 250)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'B_hypervolume_evolution.png', dpi=300, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'B_hypervolume_evolution.pdf', bbox_inches='tight')
    print(f"✓ Salvo: {OUTPUT_DIR / 'B_hypervolume_evolution.png'}")
    print("\n⚠️  NOTA: Este gráfico usa dados sintéticos para demonstração.")
    print("   Para dados reais, modifique os algoritmos para salvar HV a cada geração.")
    plt.close()

if __name__ == '__main__':
    plot_hypervolume_evolution()
