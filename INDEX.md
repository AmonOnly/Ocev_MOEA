# 📊 ÍNDICE DE ARQUIVOS - GRÁFICOS PARA RELATÓRIO MOEA

## 🚀 INÍCIO RÁPIDO

```bash
# Opção 1: Script automatizado (RECOMENDADO)
bash quick_start.sh

# Opção 2: Manual
python3 generate_plots.py
python3 generate_evolution_plot.py
```

---

## 📁 ARQUIVOS PRINCIPAIS

### 🎯 Scripts de Execução

| Arquivo | Descrição | Uso |
|---------|-----------|-----|
| **quick_start.sh** | Script bash automatizado | `bash quick_start.sh` |
| **generate_plots.py** | Gera gráficos A, C, D, E | `python3 generate_plots.py` |
| **generate_evolution_plot.py** | Gera gráfico B | `python3 generate_evolution_plot.py` |

### 📖 Documentação

| Arquivo | Conteúdo | Quando Ler |
|---------|----------|------------|
| **RESUMO.md** ⭐ | Visão geral completa | **LEIA PRIMEIRO** |
| **PLOTS_README.md** | Como usar os scripts | Antes de executar |
| **INTERPRETACAO_GRAFICOS.md** | Guia de interpretação | Ao escrever relatório |
| **INDEX.md** | Este arquivo | Navegação |

### 📊 Gráficos Gerados

| Arquivo | Gráfico | Formato |
|---------|---------|---------|
| `plots/A_pareto_fronts.*` | Fronte de Pareto | PNG + PDF |
| `plots/B_hypervolume_evolution.*` | Evolução HV | PNG + PDF |
| `plots/C_hypervolume_boxplots.*` | Boxplots HV | PNG + PDF |
| `plots/D_spacing_boxplots.*` | Boxplots Spacing | PNG + PDF |
| `plots/E_comparison_zdt1_vs_zdt3.*` | Comparação ZDT1×ZDT3 | PNG + PDF |

---

## 📚 GUIA DE LEITURA

### Para Executar os Scripts

1. **PLOTS_README.md**
   - Pré-requisitos
   - Instalação
   - Configurações
   - Solução de problemas

2. **Executar**
   ```bash
   bash quick_start.sh
   ```

### Para Escrever o Relatório

1. **RESUMO.md**
   - Visão geral dos resultados
   - Principais descobertas
   - Estrutura sugerida

2. **INTERPRETACAO_GRAFICOS.md**
   - Análise detalhada de cada gráfico
   - Tabelas de estatísticas
   - Exemplos de texto
   - Código LaTeX

3. **Revisar Gráficos**
   - Abrir arquivos em `plots/`
   - Verificar qualidade
   - Escolher versão (PNG ou PDF)

---

## 🎯 FLUXO DE TRABALHO RECOMENDADO

```
1. LEIA → RESUMO.md
   ↓
2. INSTALE → pip install numpy matplotlib
   ↓
3. EXECUTE → bash quick_start.sh
   ↓
4. REVISE → Abrir plots/A_*.png, plots/B_*.png, etc.
   ↓
5. INTERPRETE → Ler INTERPRETACAO_GRAFICOS.md
   ↓
6. ESCREVA → Usar guias e templates
   ↓
7. INCLUA → Adicionar PDFs no LaTeX
```

---

## 📊 GRÁFICOS OBRIGATÓRIOS (5 GRÁFICOS)

### ✅ A. Fronte de Pareto
- **O que é:** Soluções não-dominadas em f₁ × f₂
- **Arquivo:** `plots/A_pareto_fronts.pdf`
- **Seção:** Resultados > Análise Qualitativa

### ✅ B. Evolução do Hypervolume
- **O que é:** Convergência do HV ao longo das gerações
- **Arquivo:** `plots/B_hypervolume_evolution.pdf`
- **Seção:** Resultados > Análise de Convergência

### ✅ C. Boxplots de Hypervolume
- **O que é:** Distribuição estatística do HV
- **Arquivo:** `plots/C_hypervolume_boxplots.pdf`
- **Seção:** Resultados > Análise Quantitativa

### ✅ D. Boxplots de Spacing
- **O que é:** Distribuição estatística do Spacing
- **Arquivo:** `plots/D_spacing_boxplots.pdf`
- **Seção:** Resultados > Análise de Diversidade

### ✅ E. Comparação ZDT1 × ZDT3
- **O que é:** Análise comparativa entre problemas
- **Arquivo:** `plots/E_comparison_zdt1_vs_zdt3.pdf`
- **Seção:** Discussão > Robustez

---

## 🔍 BUSCA RÁPIDA

### "Como eu..."

| Pergunta | Resposta | Onde |
|----------|----------|------|
| ...gero os gráficos? | `bash quick_start.sh` | PLOTS_README.md |
| ...interpreto o gráfico A? | Seção "A. Fronte de Pareto" | INTERPRETACAO_GRAFICOS.md |
| ...incluo no LaTeX? | Seção "Usando no LaTeX" | INTERPRETACAO_GRAFICOS.md |
| ...explico os resultados? | Seção "Conclusões" | RESUMO.md |
| ...faço tabelas? | Seção "Tabelas Sugeridas" | INTERPRETACAO_GRAFICOS.md |
| ...ajusto configurações? | Editar início do script | PLOTS_README.md |

---

## 📈 ESTRUTURA DO RELATÓRIO

### Seção 4: RESULTADOS

```
4. RESULTADOS
   4.1 Configuração Experimental
       - Parâmetros
       - Problemas (ZDT1 e ZDT3)
       - Métricas (HV e SP)
   
   4.2 Fronte de Pareto
       → Incluir: plots/A_pareto_fronts.pdf
       → Interpretar: convergência e distribuição
   
   4.3 Convergência dos Algoritmos
       → Incluir: plots/B_hypervolume_evolution.pdf
       → Interpretar: velocidade e estabilidade
   
   4.4 Qualidade das Soluções
       → Incluir: plots/C_hypervolume_boxplots.pdf
       → Interpretar: HV médio e variação
   
   4.5 Diversidade das Soluções
       → Incluir: plots/D_spacing_boxplots.pdf
       → Interpretar: uniformidade da distribuição
   
   4.6 Análise Comparativa
       → Incluir: plots/E_comparison_zdt1_vs_zdt3.pdf
       → Interpretar: robustez entre problemas
```

### Seção 5: DISCUSSÃO

```
5. DISCUSSÃO
   5.1 Eficácia do NSGA-II
       → Por que funciona bem?
       → Comparação com Random Search
   
   5.2 Importância do Crowding Distance
       → Impacto na diversidade
       → Comparação com/sem crowding
   
   5.3 Efeito da Normalização (Fixed Bounds)
       → Como afeta métricas
       → Trade-offs
   
   5.4 Diferenças ZDT1 vs ZDT3
       → Topologia contínua vs. descontínua
       → Desafios específicos
       → Robustez do algoritmo
```

---

## 🎨 INCLUSÃO NO LaTeX

### Template Básico

```latex
% No preâmbulo
\usepackage{graphicx}

% No documento
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.9\textwidth]{plots/A_pareto_fronts.pdf}
    \caption{Fronte de Pareto obtido pelos algoritmos em ZDT1 e ZDT3.}
    \label{fig:pareto}
\end{figure}

% Referência no texto
Como mostra a Figura~\ref{fig:pareto}, o NSGA-II...
```

### Figuras Lado a Lado

```latex
\begin{figure}[htbp]
    \centering
    \begin{subfigure}[b]{0.45\textwidth}
        \includegraphics[width=\textwidth]{plots/C_hypervolume_boxplots.pdf}
        \caption{Hypervolume}
        \label{fig:hv}
    \end{subfigure}
    \hfill
    \begin{subfigure}[b]{0.45\textwidth}
        \includegraphics[width=\textwidth]{plots/D_spacing_boxplots.pdf}
        \caption{Spacing}
        \label{fig:sp}
    \end{subfigure}
    \caption{Comparação de métricas entre algoritmos.}
    \label{fig:metrics}
\end{figure}
```

---

## 📊 DADOS ESTATÍSTICOS

### ZDT1

| Algoritmo | HV | Spacing |
|-----------|------|---------|
| NSGA-II (padrão) | 0.9635 | 0.0124 |
| NSGA-II (fixed bounds) | **0.9976** | **0.0108** |
| NSGA-II (sem crowding) | 0.9789 | 0.0113 |
| Random Search | 0.0000* | 0.4652 |

### ZDT3

| Algoritmo | HV | Spacing |
|-----------|------|---------|
| NSGA-II (padrão) | **1.3686** | **0.0168** |
| NSGA-II (fixed bounds) | 1.3307 | 0.0186 |
| NSGA-II (sem crowding) | 1.3495 | 0.0183 |
| Random Search | 0.0000* | 0.3686 |

\* HV=0 devido ao ponto de referência usado

---

## ⚡ COMANDOS ÚTEIS

### Gerar Novamente

```bash
# Todos os gráficos
bash quick_start.sh

# Apenas principais
python3 generate_plots.py

# Apenas evolução
python3 generate_evolution_plot.py
```

### Verificar Arquivos

```bash
# Listar gráficos gerados
ls -lh plots/

# Contar arquivos
ls plots/ | wc -l

# Verificar PDFs
ls plots/*.pdf
```

### Visualizar

```bash
# Abrir PNG
xdg-open plots/A_pareto_fronts.png

# Abrir PDF
xdg-open plots/A_pareto_fronts.pdf

# Abrir todos
xdg-open plots/*.png
```

---

## 🐛 SOLUÇÃO DE PROBLEMAS

| Problema | Solução | Referência |
|----------|---------|------------|
| Módulo não encontrado | `pip install numpy matplotlib` | PLOTS_README.md |
| Arquivo não encontrado | Executar da raiz do projeto | PLOTS_README.md |
| Gráfico vazio | Verificar saída dos algoritmos | PLOTS_README.md |
| HV = 0 | Ajustar ponto de referência | INTERPRETACAO_GRAFICOS.md |

---

## 📞 PRECISA DE AJUDA?

1. **Leia a documentação**
   - RESUMO.md (visão geral)
   - PLOTS_README.md (uso técnico)
   - INTERPRETACAO_GRAFICOS.md (interpretação)

2. **Verifique os logs**
   - Saída do terminal ao executar scripts
   - Mensagens de erro específicas

3. **Teste componentes**
   - Scripts individuais
   - Algoritmos base (data/*.py)

---

## ✅ CHECKLIST COMPLETO

### Antes de Começar
- [ ] Python 3 instalado
- [ ] pip disponível
- [ ] numpy e matplotlib instalados
- [ ] Todos os scripts em data/ presentes

### Execução
- [ ] Executado `bash quick_start.sh` OU
- [ ] Executado `python3 generate_plots.py`
- [ ] Executado `python3 generate_evolution_plot.py`

### Verificação
- [ ] Diretório plots/ criado
- [ ] 10 arquivos gerados (5 PNG + 5 PDF)
- [ ] Sem erros no terminal
- [ ] Gráficos visualizados e corretos

### Documentação
- [ ] Lido RESUMO.md
- [ ] Lido INTERPRETACAO_GRAFICOS.md
- [ ] Entendido cada gráfico
- [ ] Estatísticas anotadas

### Relatório
- [ ] Estrutura definida
- [ ] Gráficos incluídos no LaTeX
- [ ] Interpretações escritas
- [ ] Tabelas criadas
- [ ] Conclusões redigidas

---

## 🎓 RECURSOS ADICIONAIS

### Arquivos de Referência
- `data/nsga2_zdt1.py` - Implementação NSGA-II
- `data/random_zdt1.py` - Implementação Random Search

### Conceitos-Chave
- **Hypervolume (HV):** Área dominada pelo fronte
- **Spacing (SP):** Uniformidade da distribuição
- **Crowding Distance:** Mecanismo de diversidade do NSGA-II
- **Non-dominated Sorting:** Classificação por dominância

### Papers de Referência
- Deb et al. (2002) - NSGA-II original
- Zitzler et al. (2000) - ZDT test suite

---

**Última atualização:** 26 de outubro de 2025  
**Versão:** 1.0  
**Autor:** Sistema automatizado de geração de gráficos
