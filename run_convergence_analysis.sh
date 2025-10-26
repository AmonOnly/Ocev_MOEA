#!/bin/bash

echo "======================================================================"
echo "🚀 EXECUÇÃO COMPLETA - GRÁFICOS COM DADOS REAIS DE CONVERGÊNCIA"
echo "======================================================================"
echo ""

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Passo 1: Coletar dados de convergência
echo -e "${BLUE}[PASSO 1/2]${NC} Coletando dados de convergência (HV, Spacing, Pareto)..."
echo "Tempo estimado: ~5 minutos"
echo ""
python3 generate_convergence_data.py

if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  Erro ao coletar dados de convergência${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✓ Dados de convergência coletados com sucesso!${NC}"
echo ""

# Passo 2: Gerar gráficos de convergência
echo -e "${BLUE}[PASSO 2/2]${NC} Gerando gráficos de convergência..."
echo "Tempo estimado: <1 minuto"
echo ""
python3 plot_convergence.py

if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  Erro ao gerar gráficos de convergência${NC}"
    exit 1
fi

echo ""
echo "======================================================================"
echo -e "${GREEN}✅ PROCESSO COMPLETO! DADOS REAIS COLETADOS E GRÁFICOS GERADOS${NC}"
echo "======================================================================"
echo ""
echo "📁 Arquivos gerados:"
echo ""
echo "Dados (JSON):"
echo "  convergence_data/nsga2_zdt1_convergence.json"
echo "  convergence_data/nsga2_fixedref_zdt1_convergence.json"
echo "  convergence_data/nsga2_nocrowd_zdt1_convergence.json"
echo "  convergence_data/nsga2_zdt3_convergence.json"
echo "  convergence_data/nsga2_fixedref_zdt3_convergence.json"
echo "  convergence_data/nsga2_nocrowd_zdt3_convergence.json"
echo ""
echo "Gráficos (PNG + PDF):"
echo "  plots/B_hypervolume_evolution_REAL.png/pdf"
echo "  plots/F_spacing_evolution.png/pdf"
echo "  plots/G_pareto_size_evolution.png/pdf"
echo "  plots/H_combined_metrics.png/pdf"
echo ""
echo "📖 Documentação:"
echo "  CONVERGENCE_README.md - Como usar o sistema de rastreamento"
echo "  PLOTS_README.md - Documentação de todos os gráficos"
echo ""
echo "💡 Próximos passos:"
echo "  1. Analise os gráficos em plots/"
echo "  2. Leia CONVERGENCE_README.md para interpretação"
echo "  3. Use os dados para o relatório"
echo ""
