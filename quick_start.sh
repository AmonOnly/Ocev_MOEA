#!/bin/bash
# Quick Start - Geração de Todos os Gráficos
# Execute: bash quick_start.sh

echo "=========================================="
echo "GERAÇÃO DE GRÁFICOS - RELATÓRIO MOEA"
echo "=========================================="
echo ""

# Verificar se está no diretório correto
if [ ! -d "data" ]; then
    echo "❌ ERRO: Diretório 'data/' não encontrado!"
    echo "Execute este script da raiz do projeto OCEV"
    exit 1
fi

echo "✓ Diretório correto"
echo ""

# Verificar dependências
echo "Verificando dependências Python..."
python3 -c "import numpy, matplotlib" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Instalando dependências..."
    pip install numpy matplotlib
fi
echo "✓ Dependências OK"
echo ""

# Gerar gráficos principais
echo "=========================================="
echo "1/2 Gerando gráficos principais (A, C, D, E)..."
echo "=========================================="
python3 generate_plots.py
if [ $? -ne 0 ]; then
    echo "❌ ERRO ao gerar gráficos principais"
    exit 1
fi
echo ""

# Gerar gráfico de evolução
echo "=========================================="
echo "2/2 Gerando gráfico de evolução (B)..."
echo "=========================================="
python3 generate_evolution_plot.py
if [ $? -ne 0 ]; then
    echo "❌ ERRO ao gerar gráfico de evolução"
    exit 1
fi
echo ""

# Verificar arquivos gerados
echo "=========================================="
echo "VERIFICAÇÃO DE ARQUIVOS"
echo "=========================================="
if [ -d "plots" ]; then
    echo "✓ Diretório plots/ criado"
    file_count=$(ls -1 plots/ | wc -l)
    echo "✓ $file_count arquivos gerados"
    echo ""
    echo "Arquivos:"
    ls -lh plots/ | grep -E '\.(png|pdf)$' | awk '{print "  " $9 " (" $5 ")"}'
else
    echo "❌ Diretório plots/ não encontrado!"
    exit 1
fi
echo ""

# Resumo final
echo "=========================================="
echo "✅ CONCLUÍDO COM SUCESSO!"
echo "=========================================="
echo ""
echo "📊 Gráficos gerados em: plots/"
echo ""
echo "📖 Próximos passos:"
echo "   1. Revisar gráficos em plots/"
echo "   2. Ler INTERPRETACAO_GRAFICOS.md"
echo "   3. Incluir no relatório (usar arquivos PDF)"
echo ""
echo "📝 Documentação disponível:"
echo "   - PLOTS_README.md"
echo "   - INTERPRETACAO_GRAFICOS.md"
echo "   - RESUMO.md"
echo ""
