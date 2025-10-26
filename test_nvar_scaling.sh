#!/bin/bash

# ============================================================================
# Script de Teste: NSGA-II com N = 50, 100 e 200 variáveis
# ============================================================================
# 
# Este script executa os algoritmos NSGA-II em ambos os problemas (ZDT1 e ZDT3)
# com 3 configurações de número de variáveis: N = 50, 100 e 200
#
# Conforme especificação: "Comparar o algoritmo implementado aplicando ambos 
# os problemas para N = 50, 100 e 200 sendo N o número de variáveis"
# ============================================================================

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "║          TESTE DE ESCALABILIDADE: N = 50, 100, 200 VARIÁVEIS          ║"
echo "║                    NSGA-II em ZDT1 e ZDT3                              ║"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Configurações
PROBLEMS=("ZDT1" "ZDT3")
NVARS=(50 100 200)
POP_SIZE=100
GENERATIONS=250
RUNS=10

# Diretório de saída
OUTPUT_DIR="results_nvar_comparison"
mkdir -p "$OUTPUT_DIR"

echo -e "${CYAN}📊 CONFIGURAÇÃO DO EXPERIMENTO${NC}"
echo "════════════════════════════════════════════════════════════════"
echo "Problemas:       ZDT1, ZDT3"
echo "Valores de N:    50, 100, 200"
echo "População:       $POP_SIZE"
echo "Gerações:        $GENERATIONS"
echo "Execuções:       $RUNS por configuração"
echo "Total de testes: $((2 * 3 * RUNS)) execuções"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Contador de progresso
TOTAL_EXPERIMENTS=$((2 * 3 * RUNS))
CURRENT=0

# Função para executar e salvar resultados
run_experiment() {
    local problem=$1
    local nvar=$2
    local script=$3
    local output_file=$4
    
    CURRENT=$((CURRENT + 1))
    
    echo -e "${YELLOW}[$CURRENT/$TOTAL_EXPERIMENTS]${NC} Executando: ${GREEN}$problem${NC} com N=${CYAN}$nvar${NC} variáveis"
    echo "   Script: $script"
    echo "   Saída:  $output_file"
    
    # Executar o algoritmo
    cd data/
    python3 "$script" --pop "$POP_SIZE" --gen "$GENERATIONS" --nvar "$nvar" --runs "$RUNS" > "../$output_file" 2>&1
    cd ..
    
    if [ $? -eq 0 ]; then
        echo -e "   ${GREEN}✓ Concluído com sucesso${NC}"
    else
        echo -e "   ${RED}✗ ERRO na execução${NC}"
        return 1
    fi
    echo ""
}

# Registrar início
START_TIME=$(date +%s)
echo -e "${BLUE}🚀 INICIANDO EXPERIMENTOS...${NC}"
echo ""

# ============================================================================
# EXECUTAR EXPERIMENTOS
# ============================================================================

for problem in "${PROBLEMS[@]}"; do
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  PROBLEMA: $problem${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    for nvar in "${NVARS[@]}"; do
        if [ "$problem" == "ZDT1" ]; then
            script="nsga2_zdt1.py"
        else
            script="nsga2_zdt3.py"
        fi
        
        output_file="$OUTPUT_DIR/${problem}_N${nvar}_results.txt"
        
        run_experiment "$problem" "$nvar" "$script" "$output_file"
    done
done

# ============================================================================
# PROCESSAR RESULTADOS
# ============================================================================

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
MINUTES=$((DURATION / 60))
SECONDS=$((DURATION % 60))

echo -e "${GREEN}"
echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "║                      ✅ EXPERIMENTOS CONCLUÍDOS                        ║"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${CYAN}⏱️  TEMPO TOTAL: ${MINUTES}m ${SECONDS}s${NC}"
echo ""

# Extrair resultados principais
echo -e "${BLUE}📊 RESUMO DOS RESULTADOS (Hypervolume Médio)${NC}"
echo "════════════════════════════════════════════════════════════════"

for problem in "${PROBLEMS[@]}"; do
    echo ""
    echo -e "${YELLOW}$problem:${NC}"
    printf "%-15s %-20s %-20s\n" "N Variáveis" "Hypervolume (μ)" "Spacing (μ)"
    echo "───────────────────────────────────────────────────────────────"
    
    for nvar in "${NVARS[@]}"; do
        result_file="$OUTPUT_DIR/${problem}_N${nvar}_results.txt"
        
        if [ -f "$result_file" ]; then
            # Extrair Hypervolume médio
            hv=$(grep -A 1 "Hypervolume:" "$result_file" | grep "Mean:" | awk '{print $2}' || echo "N/A")
            
            # Extrair Spacing médio
            sp=$(grep -A 1 "Spacing:" "$result_file" | grep "Mean:" | awk '{print $2}' || echo "N/A")
            
            printf "%-15s %-20s %-20s\n" "N=$nvar" "$hv" "$sp"
        else
            printf "%-15s %-20s %-20s\n" "N=$nvar" "ERRO" "ERRO"
        fi
    done
done

echo ""
echo "════════════════════════════════════════════════════════════════"

# ============================================================================
# GERAR RELATÓRIO DETALHADO
# ============================================================================

REPORT_FILE="$OUTPUT_DIR/COMPARISON_REPORT.txt"

cat > "$REPORT_FILE" << EOF
╔════════════════════════════════════════════════════════════════════════╗
║        RELATÓRIO DE COMPARAÇÃO: ESCALABILIDADE EM N VARIÁVEIS         ║
║                    NSGA-II em ZDT1 e ZDT3                              ║
╚════════════════════════════════════════════════════════════════════════╝

Data: $(date)
Tempo de execução: ${MINUTES}m ${SECONDS}s

═══════════════════════════════════════════════════════════════════════
CONFIGURAÇÃO EXPERIMENTAL
═══════════════════════════════════════════════════════════════════════

Problemas testados:     ZDT1 (contínuo), ZDT3 (descontínuo)
Valores de N:           50, 100, 200
Tamanho da população:   $POP_SIZE
Número de gerações:     $GENERATIONS
Execuções por config:   $RUNS
Total de experimentos:  $TOTAL_EXPERIMENTS

═══════════════════════════════════════════════════════════════════════
RESULTADOS CONSOLIDADOS
═══════════════════════════════════════════════════════════════════════

EOF

for problem in "${PROBLEMS[@]}"; do
    cat >> "$REPORT_FILE" << EOF

───────────────────────────────────────────────────────────────────────
PROBLEMA: $problem
───────────────────────────────────────────────────────────────────────

EOF
    
    printf "%-15s %-20s %-20s %-20s %-20s\n" \
        "N Variáveis" "HV Médio" "HV Desvio" "Spacing Médio" "Spacing Desvio" >> "$REPORT_FILE"
    echo "───────────────────────────────────────────────────────────────────────" >> "$REPORT_FILE"
    
    for nvar in "${NVARS[@]}"; do
        result_file="$OUTPUT_DIR/${problem}_N${nvar}_results.txt"
        
        if [ -f "$result_file" ]; then
            hv_mean=$(grep -A 1 "Hypervolume:" "$result_file" | grep "Mean:" | awk '{print $2}' || echo "N/A")
            hv_std=$(grep -A 2 "Hypervolume:" "$result_file" | grep "Std:" | awk '{print $2}' || echo "N/A")
            sp_mean=$(grep -A 1 "Spacing:" "$result_file" | grep "Mean:" | awk '{print $2}' || echo "N/A")
            sp_std=$(grep -A 2 "Spacing:" "$result_file" | grep "Std:" | awk '{print $2}' || echo "N/A")
            
            printf "%-15s %-20s %-20s %-20s %-20s\n" \
                "N=$nvar" "$hv_mean" "$hv_std" "$sp_mean" "$sp_std" >> "$REPORT_FILE"
        else
            printf "%-15s %-20s %-20s %-20s %-20s\n" \
                "N=$nvar" "ERRO" "ERRO" "ERRO" "ERRO" >> "$REPORT_FILE"
        fi
    done
done

cat >> "$REPORT_FILE" << EOF

═══════════════════════════════════════════════════════════════════════
ARQUIVOS GERADOS
═══════════════════════════════════════════════════════════════════════

EOF

ls -lh "$OUTPUT_DIR" >> "$REPORT_FILE"

cat >> "$REPORT_FILE" << EOF

═══════════════════════════════════════════════════════════════════════
INTERPRETAÇÃO DOS RESULTADOS
═══════════════════════════════════════════════════════════════════════

Hypervolume (HV):
  • Quanto MAIOR, melhor a aproximação da fronteira de Pareto
  • Valores esperados: ~0.95-0.97 para ZDT1, ~1.35-1.40 para ZDT3
  • Degradação com aumento de N indica maior dificuldade do problema

Spacing:
  • Quanto MENOR, melhor a uniformidade de distribuição
  • Valores esperados: ~0.01-0.02 para boa distribuição
  • Aumento com N indica dificuldade de manter diversidade

Análise esperada:
  1. N=50 → N=100: Degradação moderada (problema mais difícil)
  2. N=100 → N=200: Degradação mais acentuada (maldição dimensionalidade)
  3. ZDT3 mais sensível que ZDT1 (descontinuidade adiciona complexidade)

═══════════════════════════════════════════════════════════════════════
PRÓXIMOS PASSOS
═══════════════════════════════════════════════════════════════════════

1. Revisar os arquivos individuais em: $OUTPUT_DIR/
2. Analisar tendências de degradação com aumento de N
3. Comparar ZDT1 vs ZDT3 quanto à sensibilidade dimensional
4. Considerar aumentar gerações/população para N=200 se HV < 0.80

═══════════════════════════════════════════════════════════════════════

Fim do relatório
EOF

echo ""
echo -e "${GREEN}📄 Relatório detalhado salvo em: ${CYAN}$REPORT_FILE${NC}"
echo ""

# Mostrar localização dos arquivos
echo -e "${BLUE}📁 ARQUIVOS GERADOS${NC}"
echo "════════════════════════════════════════════════════════════════"
ls -lh "$OUTPUT_DIR"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Mostrar relatório
echo -e "${YELLOW}📖 Visualizar relatório agora? (s/N)${NC}"
read -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    cat "$REPORT_FILE"
fi

echo ""
echo -e "${GREEN}✅ TESTE DE ESCALABILIDADE CONCLUÍDO!${NC}"
echo ""
