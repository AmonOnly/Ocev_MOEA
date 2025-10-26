# Geração de Gráficos para Relatório - MOEA

Este conjunto de scripts gera todos os gráficos obrigatórios para o relatório de Algoritmos Evolutivos Multiobjetivo.

## 📋 Pré-requisitos

Instale as dependências necessárias:

```bash
pip install numpy matplotlib
```

## 🚀 Execução Rápida

### Gerar todos os gráficos principais

```bash
python3 generate_plots.py
```

Este script irá:
1. Executar todos os algoritmos (NSGA-II padrão, fixedref, sem crowding, Random Search)
2. Coletar dados de ZDT1 e ZDT3
3. Gerar os gráficos A, C, D e E
4. Salvar em formato PNG e PDF no diretório `plots/`

### Gerar gráfico de evolução (B)

```bash
python3 generate_evolution_plot.py
```

**Nota:** Por padrão, este script gera dados sintéticos para demonstração. Para dados reais, veja a seção "Modificações Avançadas" abaixo.

## 📊 Gráficos Gerados

### A. Fronte de Pareto
- **Arquivo:** `plots/A_pareto_fronts.png`
- **Descrição:** Comparação visual das soluções não-dominadas em ZDT1 e ZDT3
- **Interpretação:** 
  - NSGA-II deve ter fronte bem distribuída
  - Random Search terá soluções dispersas
  - ZDT3 mostra descontinuidades

## 📊 Gráfico B: Evolução do Hypervolume (DADOS REAIS)

**Arquivo:** `B_hypervolume_evolution_REAL.png/pdf`

Mostra como o **hypervolume (HV)** evolui ao longo das gerações para todos os algoritmos, **usando dados REAIS coletados em cada geração**.

**Como os dados são coletados:**
- Os algoritmos NSGA-II foram modificados para rastrear métricas a cada geração
- Em cada geração (1-250), calcula-se:
  - Hypervolume do Pareto atual
  - Spacing do Pareto atual
  - Tamanho do Pareto atual
- Dados salvos em `convergence_data/*.json` com média e desvio padrão de 3 execuções

**Interpretação:**
- Curvas ascendentes indicam melhoria contínua
- NSGA-II converge mais rápido e atinge HV maior
- Random Search tem HV constante e baixo (linha horizontal)
- Área sombreada mostra desvio padrão entre execuções
- Fixed bounds pode convergir de forma diferente devido à normalização fixa

### C. Boxplots de Hypervolume
- **Arquivo:** `plots/C_hypervolume_boxplots.png`
- **Descrição:** Distribuição de HV em múltiplas execuções
- **Interpretação:**
  - Maior HV = melhor qualidade
  - Menor variação = mais estável

### D. Boxplots de Spacing
- **Arquivo:** `plots/D_spacing_boxplots.png`
- **Descrição:** Uniformidade da distribuição no fronte
- **Interpretação:**
  - Menor SP = melhor distribuição
  - NSGA-II deve ter menor spacing

### E. Comparação ZDT1 × ZDT3
- **Arquivo:** `plots/E_comparison_zdt1_vs_zdt3.png`
- **Descrição:** Análise comparativa entre os dois problemas
- **Interpretação:**
  - Mostra robustez em diferentes topologias
  - Compara performance relativa

## 📈 Estatísticas Geradas

O script `generate_plots.py` também imprime estatísticas detalhadas:
- Mínimo, média, máximo e desvio padrão
- Para HV e Spacing
- Para cada algoritmo e problema

## ⚙️ Configurações

Você pode ajustar parâmetros editando o início de `generate_plots.py`:

```python
POP_SIZE = 100          # Tamanho da população
GENERATIONS = 250       # Número de gerações
N_VAR = 50             # Número de variáveis
N_RUNS = 10            # Número de execuções independentes
REF_POINT_ZDT1 = [1.2, 1.2]    # Ponto de referência para HV
REF_POINT_ZDT3 = [1.2, 1.2]
```

## 🔧 Modificações Avançadas

### Para gerar dados reais de evolução (Gráfico B)

Você precisará modificar os scripts NSGA-II para salvar HV a cada geração. Adicione ao final do loop de gerações em `nsga2()`:

```python
# No loop de gerações, adicione:
if gen % 10 == 0:  # Salvar a cada 10 gerações
    fronts_temp = non_dominated_sort(pop_objs)
    pareto_temp = [pop_objs[i] for i in fronts_temp[0]]
    hv_temp = hypervolume(pareto_temp, ref_point)
    # Salvar em arquivo ou lista
```

## 📁 Estrutura de Arquivos

```
OCEV/
├── data/
│   ├── nsga2_zdt1.py
│   ├── nsga2_zdt1_crowd_fixedref.py
│   ├── nsga2_zdt3.py
│   ├── nsga2_zdt3_crowd_fixedref.py
│   ├── random_zdt1.py
│   └── random_zdt3.py
├── generate_plots.py           # Script principal
├── generate_evolution_plot.py  # Gráfico B
├── PLOTS_README.md            # Este arquivo
└── plots/                     # Diretório de saída (criado automaticamente)
    ├── A_pareto_fronts.png
    ├── B_hypervolume_evolution.png
    ├── C_hypervolume_boxplots.png
    ├── D_spacing_boxplots.png
    └── E_comparison_zdt1_vs_zdt3.png
```

## 🎨 Personalização de Cores

As cores dos gráficos podem ser ajustadas editando:

```python
COLORS = {
    'nsga2': '#2E86AB',           # Azul
    'nsga2_fixedref': '#A23B72',  # Roxo
    'nsga2_nocrowd': '#F18F01',   # Laranja
    'random': '#C73E1D'           # Vermelho
}
```

## 📊 Formatos de Saída

Todos os gráficos são salvos em dois formatos:
- **PNG** (300 DPI) - para relatórios e apresentações
- **PDF** (vetorial) - para publicações acadêmicas

## ⏱️ Tempo de Execução

O script `generate_plots.py` executa:
- 4 algoritmos × 2 problemas × 10 runs = 80 execuções completas
- Tempo estimado: 5-15 minutos (depende do hardware)

## 🐛 Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'matplotlib'"
```bash
pip install matplotlib numpy
```

### Erro: "FileNotFoundError: data/nsga2_zdt1.py"
- Certifique-se de executar o script da raiz do projeto OCEV
- Os arquivos devem estar no diretório `data/`

### Gráficos não aparecem
- Os gráficos são salvos em arquivo, não exibidos na tela
- Verifique o diretório `plots/`

## 📝 Para o Relatório

### Seção de Resultados

Inclua os gráficos na seguinte ordem:

1. **Fronte de Pareto** (A) - mostra qualidade das soluções
2. **Evolução do HV** (B) - mostra convergência
3. **Boxplots HV** (C) - compara qualidade estatística
4. **Boxplots Spacing** (D) - compara diversidade
5. **Comparação ZDT1×ZDT3** (E) - análise cruzada

### Interpretação Recomendada

Para cada gráfico, discuta:
- **O que é observado:** descreva padrões visuais
- **Por que acontece:** explique com base nos algoritmos
- **Implicações:** o que isso significa para a qualidade da solução

### Métricas para Tabela

Use as estatísticas impressas pelo script para criar tabelas:

| Algoritmo | HV (ZDT1) | SP (ZDT1) | HV (ZDT3) | SP (ZDT3) |
|-----------|-----------|-----------|-----------|-----------|
| NSGA-II   | μ ± σ     | μ ± σ     | μ ± σ     | μ ± σ     |
| ...       | ...       | ...       | ...       | ...       |

## 📧 Suporte

Para questões ou problemas, verifique:
1. Todos os scripts estão nos diretórios corretos
2. Dependências instaladas (`pip list`)
3. Permissões de escrita no diretório `plots/`

---

## 📊 Gráficos Extras de Convergência

### Gráfico F: Evolução do Spacing
**Arquivo:** `F_spacing_evolution.png/pdf`

Mostra como a **uniformidade da distribuição** (spacing) evolui ao longo das gerações.

**Interpretação:**
- Spacing menor = distribuição mais uniforme (melhor)
- Curvas descendentes indicam melhoria na diversidade
- NSGA-II com crowding distance mantém melhor spacing
- Sem crowding, o spacing pode piorar ao longo do tempo

### Gráfico G: Evolução do Tamanho do Pareto
**Arquivo:** `G_pareto_size_evolution.png/pdf`

Mostra como o **número de soluções no Pareto** evolui ao longo das gerações.

**Interpretação:**
- Tamanho estável indica convergência
- Crescimento inicial é normal (descoberta de novas soluções)
- NSGA-II sem crowding pode ter Pareto menor (menos diversidade)
- Tamanho muito grande pode indicar falta de convergência

### Gráfico H: Métricas Combinadas
**Arquivo:** `H_combined_metrics.png/pdf`

Painel com **todas as métricas (HV e Spacing)** para ZDT1 e ZDT3 em um único gráfico.

**Interpretação:**
- Visão geral da performance de cada algoritmo
- Permite comparação direta entre ZDT1 e ZDT3
- Útil para análise de tendências globais

---

**Última atualização:** 26 de outubro de 2025
