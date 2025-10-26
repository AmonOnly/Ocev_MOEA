#!/usr/bin/env python3
"""
Script para gerar gráficos de análise de escalabilidade (N variáveis)

Gera os seguintes gráficos:
- I: Degradação de Hypervolume vs N (ZDT1 e ZDT3)
- J: Degradação de Spacing vs N (ZDT1 e ZDT3)
- K: Comparação lado-a-lado de fronteiras para diferentes N

Autor: Sistema OCEV
Data: 26 de outubro de 2025
"""

import json
import re
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import sys

# Configuração de estilo
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['lines.linewidth'] = 2.5

# Cores consistentes
COLORS = {
    'nsga2': '#2E86AB',      # Azul
    'fixed': '#A23B72',      # Roxo
    'nocrowd': '#F18F01',    # Laranja
    'random': '#C73E1D'      # Vermelho
}

NVAR_COLORS = {
    50: '#1B9E77',   # Verde
    100: '#D95F02',  # Laranja
    200: '#7570B3'   # Roxo
}

def load_results(results_dir):
    """Carrega resultados dos experimentos de escalabilidade"""
    results = {}
    
    problems = ['ZDT1', 'ZDT3']
    nvars = [50, 100, 200]
    
    for problem in problems:
        results[problem] = {}
        for nvar in nvars:
            filename = f"{problem}_N{nvar}_results.txt"
            filepath = Path(results_dir) / filename
            
            if filepath.exists():
                with open(filepath, 'r') as f:
                    content = f.read()
                    
                # Procurar por estatísticas agregadas (Mean/Std)
                hv_values = []
                sp_values = []
                
                # Extrair valores individuais de cada run
                for line in content.split('\n'):
                    if line.startswith('Run '):
                        # Extrair hv e spacing da linha
                        hv_match = re.search(r'hv=([\d.]+)', line)
                        sp_match = re.search(r'spacing=([\d.]+)', line)
                        
                        if hv_match:
                            hv_values.append(float(hv_match.group(1)))
                        if sp_match:
                            sp_values.append(float(sp_match.group(1)))
                
                # Calcular estatísticas
                if hv_values:
                    hv_mean = np.mean(hv_values)
                    hv_std = np.std(hv_values)
                    sp_mean = np.mean(sp_values)
                    sp_std = np.std(sp_values)
                    
                    results[problem][nvar] = {
                        'hv_mean': hv_mean,
                        'hv_std': hv_std,
                        'sp_mean': sp_mean,
                        'sp_std': sp_std
                    }
                else:
                    print(f"⚠️  Nenhum dado encontrado em: {filepath}")
                    results[problem][nvar] = None
            else:
                print(f"⚠️  Arquivo não encontrado: {filepath}")
                results[problem][nvar] = None
    
    return results

def plot_hypervolume_scaling(results, output_dir):
    """Gráfico I: Degradação de Hypervolume vs N"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    for idx, problem in enumerate(['ZDT1', 'ZDT3']):
        ax = axes[idx]
        
        nvars = [50, 100, 200]
        hv_means = []
        hv_stds = []
        
        for nvar in nvars:
            if results[problem][nvar] and results[problem][nvar]['hv_mean']:
                hv_means.append(results[problem][nvar]['hv_mean'])
                hv_stds.append(results[problem][nvar]['hv_std'])
            else:
                hv_means.append(0)
                hv_stds.append(0)
        
        # Plot com barras de erro
        ax.errorbar(nvars, hv_means, yerr=hv_stds, 
                   marker='o', markersize=10, capsize=5, capthick=2,
                   color=COLORS['nsga2'], linewidth=2.5, label='NSGA-II')
        
        # Linha de tendência
        if any(hv_means):
            z = np.polyfit(nvars, hv_means, 2)
            p = np.poly1d(z)
            x_smooth = np.linspace(50, 200, 100)
            ax.plot(x_smooth, p(x_smooth), '--', color=COLORS['nsga2'], 
                   alpha=0.5, linewidth=1.5, label='Tendência')
        
        ax.set_xlabel('Número de Variáveis (N)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Hypervolume Médio', fontsize=12, fontweight='bold')
        ax.set_title(f'{problem}', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_xticks(nvars)
        ax.legend(loc='best')
        
        # Adicionar percentual de degradação
        if hv_means[0] > 0 and hv_means[-1] > 0:
            degradation = ((hv_means[0] - hv_means[-1]) / hv_means[0]) * 100
            ax.text(0.05, 0.95, f'Degradação N50→N200: {degradation:.1f}%',
                   transform=ax.transAxes, fontsize=10, verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.suptitle('Escalabilidade do NSGA-II: Impacto do Número de Variáveis no Hypervolume',
                fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    # Salvar
    output_path = Path(output_dir)
    plt.savefig(output_path / 'I_hypervolume_nvar_scaling.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_path / 'I_hypervolume_nvar_scaling.pdf', bbox_inches='tight')
    plt.close()
    
    print(f"✅ Gráfico I salvo: I_hypervolume_nvar_scaling.png/pdf")

def plot_spacing_scaling(results, output_dir):
    """Gráfico J: Degradação de Spacing vs N"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    for idx, problem in enumerate(['ZDT1', 'ZDT3']):
        ax = axes[idx]
        
        nvars = [50, 100, 200]
        sp_means = []
        sp_stds = []
        
        for nvar in nvars:
            if results[problem][nvar] and results[problem][nvar]['sp_mean']:
                sp_means.append(results[problem][nvar]['sp_mean'])
                sp_stds.append(results[problem][nvar]['sp_std'])
            else:
                sp_means.append(0)
                sp_stds.append(0)
        
        # Plot com barras de erro
        ax.errorbar(nvars, sp_means, yerr=sp_stds, 
                   marker='s', markersize=10, capsize=5, capthick=2,
                   color=COLORS['fixed'], linewidth=2.5, label='NSGA-II')
        
        # Linha de tendência
        if any(sp_means):
            z = np.polyfit(nvars, sp_means, 2)
            p = np.poly1d(z)
            x_smooth = np.linspace(50, 200, 100)
            ax.plot(x_smooth, p(x_smooth), '--', color=COLORS['fixed'], 
                   alpha=0.5, linewidth=1.5, label='Tendência')
        
        ax.set_xlabel('Número de Variáveis (N)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Spacing Médio', fontsize=12, fontweight='bold')
        ax.set_title(f'{problem}', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_xticks(nvars)
        ax.legend(loc='best')
        
        # Adicionar percentual de piora
        if sp_means[0] > 0 and sp_means[-1] > 0:
            increase = ((sp_means[-1] - sp_means[0]) / sp_means[0]) * 100
            ax.text(0.05, 0.95, f'Aumento N50→N200: {increase:.1f}%',
                   transform=ax.transAxes, fontsize=10, verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    
    plt.suptitle('Escalabilidade do NSGA-II: Impacto do Número de Variáveis no Spacing',
                fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    # Salvar
    output_path = Path(output_dir)
    plt.savefig(output_path / 'J_spacing_nvar_scaling.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_path / 'J_spacing_nvar_scaling.pdf', bbox_inches='tight')
    plt.close()
    
    print(f"✅ Gráfico J salvo: J_spacing_nvar_scaling.png/pdf")

def plot_combined_scaling(results, output_dir):
    """Gráfico K: Comparação combinada (HV e Spacing) para ambos problemas"""
    fig = plt.figure(figsize=(14, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    
    nvars = [50, 100, 200]
    
    # ZDT1 - Hypervolume
    ax1 = fig.add_subplot(gs[0, 0])
    hv_means = [results['ZDT1'][n]['hv_mean'] if (results['ZDT1'][n] and results['ZDT1'][n]['hv_mean'] is not None) else 0 for n in nvars]
    hv_stds = [results['ZDT1'][n]['hv_std'] if (results['ZDT1'][n] and results['ZDT1'][n]['hv_std'] is not None) else 0 for n in nvars]
    
    bars1 = ax1.bar(range(len(nvars)), hv_means, yerr=hv_stds, 
                    color=[NVAR_COLORS[n] for n in nvars], 
                    capsize=5, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Hypervolume', fontsize=12, fontweight='bold')
    ax1.set_title('ZDT1 - Hypervolume', fontsize=13, fontweight='bold')
    ax1.set_xticks(range(len(nvars)))
    ax1.set_xticklabels([f'N={n}' for n in nvars])
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Adicionar valores nas barras
    for i, (bar, val) in enumerate(zip(bars1, hv_means)):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.3f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # ZDT1 - Spacing
    ax2 = fig.add_subplot(gs[0, 1])
    sp_means = [results['ZDT1'][n]['sp_mean'] if (results['ZDT1'][n] and results['ZDT1'][n]['sp_mean'] is not None) else 0 for n in nvars]
    sp_stds = [results['ZDT1'][n]['sp_std'] if (results['ZDT1'][n] and results['ZDT1'][n]['sp_std'] is not None) else 0 for n in nvars]
    
    bars2 = ax2.bar(range(len(nvars)), sp_means, yerr=sp_stds,
                    color=[NVAR_COLORS[n] for n in nvars],
                    capsize=5, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax2.set_ylabel('Spacing', fontsize=12, fontweight='bold')
    ax2.set_title('ZDT1 - Spacing', fontsize=13, fontweight='bold')
    ax2.set_xticks(range(len(nvars)))
    ax2.set_xticklabels([f'N={n}' for n in nvars])
    ax2.grid(True, alpha=0.3, axis='y')
    
    for i, (bar, val) in enumerate(zip(bars2, sp_means)):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.4f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # ZDT3 - Hypervolume
    ax3 = fig.add_subplot(gs[1, 0])
    hv_means = [results['ZDT3'][n]['hv_mean'] if (results['ZDT3'][n] and results['ZDT3'][n]['hv_mean'] is not None) else 0 for n in nvars]
    hv_stds = [results['ZDT3'][n]['hv_std'] if (results['ZDT3'][n] and results['ZDT3'][n]['hv_std'] is not None) else 0 for n in nvars]
    
    bars3 = ax3.bar(range(len(nvars)), hv_means, yerr=hv_stds,
                    color=[NVAR_COLORS[n] for n in nvars],
                    capsize=5, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax3.set_ylabel('Hypervolume', fontsize=12, fontweight='bold')
    ax3.set_title('ZDT3 - Hypervolume', fontsize=13, fontweight='bold')
    ax3.set_xticks(range(len(nvars)))
    ax3.set_xticklabels([f'N={n}' for n in nvars])
    ax3.grid(True, alpha=0.3, axis='y')
    
    for i, (bar, val) in enumerate(zip(bars3, hv_means)):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.3f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # ZDT3 - Spacing
    ax4 = fig.add_subplot(gs[1, 1])
    sp_means = [results['ZDT3'][n]['sp_mean'] if (results['ZDT3'][n] and results['ZDT3'][n]['sp_mean'] is not None) else 0 for n in nvars]
    sp_stds = [results['ZDT3'][n]['sp_std'] if (results['ZDT3'][n] and results['ZDT3'][n]['sp_std'] is not None) else 0 for n in nvars]
    
    bars4 = ax4.bar(range(len(nvars)), sp_means, yerr=sp_stds,
                    color=[NVAR_COLORS[n] for n in nvars],
                    capsize=5, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax4.set_ylabel('Spacing', fontsize=12, fontweight='bold')
    ax4.set_title('ZDT3 - Spacing', fontsize=13, fontweight='bold')
    ax4.set_xticks(range(len(nvars)))
    ax4.set_xticklabels([f'N={n}' for n in nvars])
    ax4.grid(True, alpha=0.3, axis='y')
    
    for i, (bar, val) in enumerate(zip(bars4, sp_means)):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.4f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # Legenda global
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=NVAR_COLORS[n], edgecolor='black', 
                            label=f'N={n}') for n in nvars]
    fig.legend(handles=legend_elements, loc='upper center', 
              ncol=3, fontsize=11, frameon=True, bbox_to_anchor=(0.5, 0.98))
    
    plt.suptitle('Análise Comparativa de Escalabilidade: NSGA-II em ZDT1 e ZDT3',
                fontsize=16, fontweight='bold', y=0.995)
    
    # Salvar
    output_path = Path(output_dir)
    plt.savefig(output_path / 'K_combined_nvar_comparison.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_path / 'K_combined_nvar_comparison.pdf', bbox_inches='tight')
    plt.close()
    
    print(f"✅ Gráfico K salvo: K_combined_nvar_comparison.png/pdf")

def main():
    print("\n" + "="*70)
    print("  GERAÇÃO DE GRÁFICOS DE ESCALABILIDADE (N VARIÁVEIS)")
    print("="*70 + "\n")
    
    # Diretórios
    results_dir = Path('results_nvar_comparison')
    output_dir = Path('plots')
    output_dir.mkdir(exist_ok=True)
    
    # Verificar se diretório de resultados existe
    if not results_dir.exists():
        print(f"❌ ERRO: Diretório {results_dir} não encontrado!")
        print(f"   Execute primeiro: bash test_nvar_scaling.sh")
        sys.exit(1)
    
    # Carregar resultados
    print("📂 Carregando resultados...")
    results = load_results(results_dir)
    
    # Verificar se há dados
    has_data = False
    for problem in results:
        for nvar in results[problem]:
            if results[problem][nvar]:
                has_data = True
                break
    
    if not has_data:
        print("❌ ERRO: Nenhum resultado encontrado!")
        print("   Execute: bash test_nvar_scaling.sh")
        sys.exit(1)
    
    print(f"✅ Resultados carregados\n")
    
    # Gerar gráficos
    print("📊 Gerando gráficos...\n")
    
    plot_hypervolume_scaling(results, output_dir)
    plot_spacing_scaling(results, output_dir)
    plot_combined_scaling(results, output_dir)
    
    print("\n" + "="*70)
    print("  ✅ GRÁFICOS DE ESCALABILIDADE GERADOS COM SUCESSO!")
    print("="*70)
    print(f"\n📁 Gráficos salvos em: {output_dir}/")
    print("   • I_hypervolume_nvar_scaling.png/pdf")
    print("   • J_spacing_nvar_scaling.png/pdf")
    print("   • K_combined_nvar_comparison.png/pdf")
    print("\n")

if __name__ == '__main__':
    main()
