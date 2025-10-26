#!/bin/bash

# ============================================================================
# Script Master: Execução Completa de Experimentos de Escalabilidade
# ============================================================================
#
# Este script executa:
# 1. Testes com N = 50, 100, 200 variáveis
# 2. Geração de gráficos de escalabilidade
# 3. Atualização do relatório LaTeX
#
# ============================================================================

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
cat << "EOF"
╔════════════════════════════════════════════════════════════════════════╗
║          EXPERIMENTOS COMPLETOS: ESCALABILIDADE NSGA-II                ║
║                    N = 50, 100, 200 Variáveis                          ║
╚════════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# ============================================================================
# ETAPA 1: EXECUTAR TESTES DE ESCALABILIDADE
# ============================================================================

echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}  ETAPA 1: EXECUTAR TESTES DE ESCALABILIDADE${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo ""

if [ -d "results_nvar_comparison" ]; then
    echo -e "${YELLOW}⚠️  Diretório results_nvar_comparison já existe${NC}"
    read -p "Deseja executar novamente os testes? (s/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        echo -e "${BLUE}🔄 Removendo resultados antigos...${NC}"
        rm -rf results_nvar_comparison
        echo -e "${GREEN}✓ Pronto para novos testes${NC}"
        RUN_TESTS=true
    else
        echo -e "${YELLOW}⏭️  Pulando execução de testes (usando resultados existentes)${NC}"
        RUN_TESTS=false
    fi
else
    RUN_TESTS=true
fi

if [ "$RUN_TESTS" = true ]; then
    echo ""
    echo -e "${BLUE}🚀 Executando testes de escalabilidade...${NC}"
    echo -e "${YELLOW}   Isso pode levar 30-40 minutos (60 execuções)${NC}"
    echo ""
    
    read -p "Continuar? (S/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        bash test_nvar_scaling.sh
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Testes concluídos com sucesso${NC}"
        else
            echo -e "${RED}❌ ERRO na execução dos testes${NC}"
            exit 1
        fi
    else
        echo -e "${RED}❌ Execução cancelada${NC}"
        exit 0
    fi
else
    echo -e "${GREEN}✓ Usando resultados existentes${NC}"
fi

echo ""

# ============================================================================
# ETAPA 2: GERAR GRÁFICOS DE ESCALABILIDADE
# ============================================================================

echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}  ETAPA 2: GERAR GRÁFICOS DE ESCALABILIDADE${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo ""

if [ ! -d "results_nvar_comparison" ]; then
    echo -e "${RED}❌ ERRO: Diretório results_nvar_comparison não encontrado!${NC}"
    echo -e "   Execute primeiro a Etapa 1 (testes)"
    exit 1
fi

echo -e "${BLUE}📊 Gerando gráficos I, J, K...${NC}"
python3 plot_nvar_scaling.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Gráficos gerados com sucesso${NC}"
else
    echo -e "${RED}❌ ERRO na geração de gráficos${NC}"
    exit 1
fi

echo ""

# ============================================================================
# ETAPA 3: VERIFICAR GRÁFICOS GERADOS
# ============================================================================

echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}  ETAPA 3: VERIFICAR GRÁFICOS${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo ""

PLOTS_DIR="plots"
EXPECTED_PLOTS=(
    "I_hypervolume_nvar_scaling.pdf"
    "J_spacing_nvar_scaling.pdf"
    "K_combined_nvar_comparison.pdf"
)

ALL_PLOTS_OK=true

for plot in "${EXPECTED_PLOTS[@]}"; do
    if [ -f "$PLOTS_DIR/$plot" ]; then
        SIZE=$(du -h "$PLOTS_DIR/$plot" | cut -f1)
        echo -e "${GREEN}✓${NC} $plot (${SIZE})"
    else
        echo -e "${RED}✗${NC} $plot ${RED}NÃO ENCONTRADO${NC}"
        ALL_PLOTS_OK=false
    fi
done

echo ""

if [ "$ALL_PLOTS_OK" = true ]; then
    echo -e "${GREEN}✅ Todos os gráficos de escalabilidade foram gerados${NC}"
else
    echo -e "${RED}❌ Alguns gráficos estão faltando${NC}"
    exit 1
fi

# ============================================================================
# ETAPA 4: ATUALIZAR RELATÓRIO LATEX
# ============================================================================

echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}  ETAPA 4: RELATÓRIO LATEX${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo ""

if [ ! -f "relatorio_latex/sections/11_scalability.tex" ]; then
    echo -e "${RED}❌ ERRO: Seção de escalabilidade não encontrada${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Seção 11_scalability.tex criada"
echo -e "${GREEN}✓${NC} main.tex atualizado para incluir seção"
echo ""

echo -e "${BLUE}📄 Deseja compilar o relatório LaTeX agora? (s/N)${NC}"
read -n 1 -r
echo

if [[ $REPLY =~ ^[Ss]$ ]]; then
    cd relatorio_latex/
    bash compile.sh
    cd ..
fi

# ============================================================================
# RESUMO FINAL
# ============================================================================

echo ""
echo -e "${GREEN}"
cat << "EOF"
╔════════════════════════════════════════════════════════════════════════╗
║                    ✅ PROCESSO COMPLETO!                               ║
╚════════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${BLUE}📊 RESUMO DO QUE FOI FEITO:${NC}"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo -e "1. ${GREEN}✓${NC} Testes de escalabilidade (N=50, 100, 200)"
echo -e "   📁 Resultados em: ${CYAN}results_nvar_comparison/${NC}"
echo ""
echo -e "2. ${GREEN}✓${NC} Gráficos de escalabilidade gerados"
echo -e "   📊 I_hypervolume_nvar_scaling.pdf"
echo -e "   📊 J_spacing_nvar_scaling.pdf"
echo -e "   📊 K_combined_nvar_comparison.pdf"
echo ""
echo -e "3. ${GREEN}✓${NC} Relatório LaTeX atualizado"
echo -e "   📄 Nova seção: 11_scalability.tex"
echo -e "   📄 Main.tex atualizado"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""

echo -e "${MAGENTA}📈 RESULTADOS PRINCIPAIS:${NC}"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Tentar extrair e mostrar resultados principais
if [ -f "results_nvar_comparison/COMPARISON_REPORT.txt" ]; then
    echo -e "${CYAN}ZDT1:${NC}"
    grep -A 3 "PROBLEMA: ZDT1" results_nvar_comparison/COMPARISON_REPORT.txt | tail -3 || true
    echo ""
    echo -e "${CYAN}ZDT3:${NC}"
    grep -A 3 "PROBLEMA: ZDT3" results_nvar_comparison/COMPARISON_REPORT.txt | tail -3 || true
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""

echo -e "${YELLOW}📚 PRÓXIMOS PASSOS:${NC}"
echo ""
echo "1. Revisar relatório consolidado:"
echo -e "   ${CYAN}cat results_nvar_comparison/COMPARISON_REPORT.txt${NC}"
echo ""
echo "2. Visualizar gráficos:"
echo -e "   ${CYAN}xdg-open plots/I_hypervolume_nvar_scaling.pdf${NC}"
echo ""
echo "3. Compilar relatório final:"
echo -e "   ${CYAN}cd relatorio_latex/ && bash compile.sh${NC}"
echo ""
echo "4. Revisar seção de escalabilidade no PDF:"
echo -e "   ${CYAN}xdg-open relatorio_latex/main.pdf${NC}"
echo ""

echo "════════════════════════════════════════════════════════════════"
echo ""
echo -e "${GREEN}🎉 EXPERIMENTOS DE ESCALABILIDADE CONCLUÍDOS!${NC}"
echo ""
