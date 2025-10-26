#!/bin/bash

# ============================================================================
# Script de Compilação do Relatório LaTeX
# ============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         COMPILAÇÃO DO RELATÓRIO TÉCNICO NSGA-II                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if pdflatex is installed
if ! command -v pdflatex &> /dev/null; then
    echo -e "${RED}❌ ERRO: pdflatex não encontrado!${NC}"
    echo ""
    echo "Instale TeX Live ou MiKTeX:"
    echo "  Ubuntu/Debian: sudo apt-get install texlive-full"
    echo "  macOS:         brew install --cask mactex"
    echo "  Windows:       https://miktex.org/"
    exit 1
fi

# Check if main.tex exists
if [ ! -f "main.tex" ]; then
    echo -e "${RED}❌ ERRO: main.tex não encontrado!${NC}"
    echo "Execute este script na pasta relatorio_latex/"
    exit 1
fi

# Check if plots directory exists
if [ ! -d "../plots" ]; then
    echo -e "${YELLOW}⚠️  AVISO: Pasta ../plots/ não encontrada${NC}"
    echo "Alguns gráficos podem não ser incluídos no PDF"
    read -p "Continuar mesmo assim? (s/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        exit 1
    fi
fi

# Check for required plot files
REQUIRED_PLOTS=(
    "A_pareto_fronts.pdf"
    "B_hypervolume_evolution_REAL.pdf"
    "C_hypervolume_boxplots.pdf"
    "D_spacing_boxplots.pdf"
    "E_zdt1_vs_zdt3.pdf"
    "F_spacing_evolution.pdf"
    "G_pareto_size_evolution.pdf"
    "H_combined_metrics.pdf"
)

MISSING_PLOTS=0
for plot in "${REQUIRED_PLOTS[@]}"; do
    if [ ! -f "../plots/$plot" ]; then
        echo -e "${YELLOW}⚠️  Faltando: ../plots/$plot${NC}"
        MISSING_PLOTS=$((MISSING_PLOTS + 1))
    fi
done

if [ $MISSING_PLOTS -gt 0 ]; then
    echo -e "${YELLOW}⚠️  $MISSING_PLOTS gráfico(s) faltando${NC}"
    echo "Execute: cd .. && python3 plot_convergence.py && python3 first.py"
    read -p "Continuar mesmo assim? (s/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        exit 1
    fi
fi

echo ""
echo -e "${BLUE}📄 Compilando documento...${NC}"
echo ""

# Clean previous auxiliary files
echo "🧹 Limpando arquivos auxiliares antigos..."
rm -f main.aux main.log main.out main.toc main.lof main.lot main.bbl main.blg

# First compilation
echo ""
echo "🔨 Compilação 1/2 (gerando estrutura)..."
pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Compilação 1/2 concluída${NC}"
else
    echo -e "${RED}❌ ERRO na primeira compilação!${NC}"
    echo "Verifique o arquivo main.log para detalhes"
    pdflatex -interaction=nonstopmode main.tex | tail -20
    exit 1
fi

# Second compilation (for cross-references)
echo ""
echo "🔨 Compilação 2/2 (resolvendo referências)..."
pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Compilação 2/2 concluída${NC}"
else
    echo -e "${RED}❌ ERRO na segunda compilação!${NC}"
    echo "Verifique o arquivo main.log para detalhes"
    pdflatex -interaction=nonstopmode main.tex | tail -20
    exit 1
fi

# Check if PDF was generated
if [ -f "main.pdf" ]; then
    PDF_SIZE=$(du -h main.pdf | cut -f1)
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                 ✅ COMPILAÇÃO CONCLUÍDA COM SUCESSO!           ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "📊 Arquivo gerado: ${GREEN}main.pdf${NC} (${PDF_SIZE})"
    echo ""
    
    # Count pages (if pdfinfo is available)
    if command -v pdfinfo &> /dev/null; then
        PAGES=$(pdfinfo main.pdf | grep "Pages:" | awk '{print $2}')
        echo -e "📄 Número de páginas: ${GREEN}$PAGES${NC}"
    fi
    
    # Optional: Open PDF
    echo ""
    read -p "Deseja abrir o PDF agora? (S/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        if command -v xdg-open &> /dev/null; then
            xdg-open main.pdf &
        elif command -v open &> /dev/null; then
            open main.pdf &
        elif command -v start &> /dev/null; then
            start main.pdf &
        else
            echo "Não foi possível abrir automaticamente. Abra manualmente: main.pdf"
        fi
    fi
    
    # Optional: Clean auxiliary files
    echo ""
    read -p "Deseja limpar arquivos auxiliares (.aux, .log, etc.)? (S/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        rm -f main.aux main.log main.out main.toc main.lof main.lot main.bbl main.blg
        echo -e "${GREEN}✅ Arquivos auxiliares removidos${NC}"
    fi
    
else
    echo -e "${RED}❌ ERRO: PDF não foi gerado!${NC}"
    echo "Verifique o arquivo main.log para detalhes do erro"
    exit 1
fi

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""
