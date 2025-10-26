# Relatório LaTeX - Análise Experimental NSGA-II

## 📄 Sobre o Documento

Relatório técnico completo da análise experimental do algoritmo NSGA-II aplicado aos problemas de benchmark ZDT1 e ZDT3, incluindo análise de convergência em tempo real.

**Título**: Análise Experimental do Algoritmo NSGA-II: Estudo Comparativo de Variantes em Problemas de Benchmark ZDT

**Autor**: Sistema de Experimentação OCEV

**Data**: 26 de outubro de 2025

---

## 📁 Estrutura do Projeto

```
relatorio_latex/
├── main.tex                          # Documento principal (orquestra tudo)
├── sections/                         # Seções modulares
│   ├── 00_titlepage.tex             # Página de título
│   ├── 01_abstract.tex              # Resumo executivo
│   ├── 02_introduction.tex          # Introdução (contexto, MOO, NSGA-II)
│   ├── 03_methodology.tex           # Metodologia (algoritmos, métricas)
│   ├── 04_experimental_setup.tex    # Configuração experimental
│   ├── 05_results.tex               # Resultados (análise quali/quanti)
│   ├── 06_convergence_analysis.tex  # Análise de convergência
│   ├── 07_discussion.tex            # Discussão (interpretação, limitações)
│   ├── 08_conclusion.tex            # Conclusão
│   └── 09_references.tex            # Referências bibliográficas
└── README.md                         # Este arquivo
```

---

## 🛠️ Compilação

### Pré-requisitos

O documento requer uma distribuição LaTeX completa:

- **Linux**: TeX Live
  ```bash
  sudo apt-get install texlive-full
  ```

- **macOS**: MacTeX
  ```bash
  brew install --cask mactex
  ```

- **Windows**: MiKTeX ou TeX Live
  - Download: https://miktex.org/ ou https://www.tug.org/texlive/

### Pacotes LaTeX Necessários

O documento usa os seguintes pacotes (geralmente incluídos em distribuições completas):

- `babel` (português)
- `inputenc` (UTF-8)
- `geometry` (margens)
- `graphicx` (figuras)
- `amsmath`, `amssymb` (matemática)
- `booktabs` (tabelas)
- `hyperref` (links)
- `fancyhdr` (cabeçalhos/rodapés)
- `xcolor` (cores)
- `float`, `caption`, `subcaption` (posicionamento de figuras)

### Compilar o Documento

#### Opção 1: pdflatex (Recomendado)

```bash
cd relatorio_latex
pdflatex main.tex
pdflatex main.tex  # Segunda passagem para referências
```

**Saída**: `main.pdf`

#### Opção 2: Makefile (se disponível)

```bash
cd relatorio_latex
make
```

#### Opção 3: latexmk (Automático)

```bash
cd relatorio_latex
latexmk -pdf main.tex
```

Limpar arquivos auxiliares:
```bash
latexmk -c
```

### Compilação com Overleaf

1. Faça upload de todos os arquivos `.tex` mantendo a estrutura de pastas
2. Faça upload da pasta `../plots/` com todos os PDFs dos gráficos
3. Configure o compilador para **pdfLaTeX**
4. Compile (botão verde "Recompile")

---

## 📊 Requisitos de Dados

O relatório referencia **8 gráficos** que devem estar disponíveis em `../plots/`:

### Gráficos Obrigatórios (formato PDF preferencial)

```
../plots/A_pareto_fronts.pdf
../plots/B_hypervolume_evolution_REAL.pdf
../plots/C_hypervolume_boxplots.pdf
../plots/D_spacing_boxplots.pdf
../plots/E_zdt1_vs_zdt3.pdf
../plots/F_spacing_evolution.pdf
../plots/G_pareto_size_evolution.pdf
../plots/H_combined_metrics.pdf
```

### Gerar os Gráficos

Se os gráficos não existirem:

```bash
cd ..
python3 plot_convergence.py  # Gera gráficos B, F, G, H
python3 first.py              # Gera gráficos A, C, D, E
```

---

## 📝 Estrutura do Conteúdo

### Seções do Relatório

| Seção | Arquivo | Páginas Aprox. | Conteúdo |
|-------|---------|----------------|----------|
| Capa | `00_titlepage.tex` | 1 | Informações do experimento |
| Resumo | `01_abstract.tex` | 1 | Objetivos, metodologia, resultados-chave |
| Introdução | `02_introduction.tex` | 6-7 | MOO, NSGA-II, ZDT, motivação |
| Metodologia | `03_methodology.tex` | 5-6 | Algoritmos, métricas, rastreamento |
| Setup Experimental | `04_experimental_setup.tex` | 4-5 | Parâmetros, problemas, protocolo |
| Resultados | `05_results.tex` | 6-7 | Análise quali/quanti, tabelas, gráficos |
| Convergência | `06_convergence_analysis.tex` | 8-9 | Dinâmica evolutiva, fases, insights |
| Discussão | `07_discussion.tex` | 7-8 | Interpretação, limitações, futuros |
| Conclusão | `08_conclusion.tex` | 3-4 | Síntese, contribuições, considerações |
| Referências | `09_references.tex` | 2-3 | Bibliografia, recursos, ferramentas |

**Total estimado**: ~45-50 páginas

---

## 🎨 Personalização

### Alterar Título/Autor

Edite `sections/00_titlepage.tex`:

```latex
\textbf{\LARGE Seu Título Aqui} \\[0.5cm]
```

### Ajustar Margens

Edite `main.tex`:

```latex
\usepackage[left=3cm, right=2cm, top=3cm, bottom=2cm]{geometry}
```

### Mudar Fonte do Documento

Adicione ao preâmbulo de `main.tex`:

```latex
\usepackage{times}  % Times New Roman
% ou
\usepackage{helvet} % Helvetica
```

### Alterar Idioma

Mude em `main.tex`:

```latex
\usepackage[english]{babel}  % Para inglês
```

E traduza o conteúdo dos arquivos em `sections/`.

---

## 🔍 Solução de Problemas

### Erro: "File '...pdf' not found"

**Causa**: Gráficos não encontrados em `../plots/`

**Solução**: 
```bash
cd ..
python3 plot_convergence.py
python3 first.py
```

### Erro: "Undefined control sequence \hlv"

**Causa**: Comando customizado não definido

**Solução**: Verifique que `main.tex` contém:
```latex
\newcommand{\hlv}{\textit{Hypervolume}}
```

### Erro: "Package babel Error: Unknown option 'portuguese'"

**Causa**: Pacote babel desatualizado ou não instalado

**Solução**:
```bash
sudo apt-get install texlive-lang-portuguese
```

### Erro: "! LaTeX Error: File 'booktabs.sty' not found"

**Causa**: Pacotes faltando

**Solução**: Instale distribuição completa ou manualmente:
```bash
sudo apt-get install texlive-latex-extra
```

### Referências cruzadas com "??"

**Causa**: Apenas uma compilação executada

**Solução**: Compile **duas vezes**:
```bash
pdflatex main.tex
pdflatex main.tex
```

---

## 📤 Exportação

### Para Submissão (PDF)

Após compilação bem-sucedida:

```bash
cp main.pdf Relatorio_NSGA2_ZDT_Analise_Completa.pdf
```

### Para Edição Colaborativa

**Overleaf**: 
1. Compacte a pasta: `zip -r relatorio.zip relatorio_latex/ plots/`
2. Faça upload no Overleaf

**Git**:
```bash
git add relatorio_latex/
git commit -m "Add complete LaTeX report"
git push
```

---

## 📊 Informações Adicionais

### Estatísticas do Documento

- **Linhas de LaTeX**: ~2.500
- **Figuras**: 8
- **Tabelas**: 5
- **Referências**: 20
- **Seções**: 9
- **Páginas**: ~45-50

### Dados Experimentais Incluídos

- **Execuções finais**: 10 por algoritmo (40 total)
- **Execuções de convergência**: 3 por algoritmo (12 total)
- **Pontos de dados rastreados**: 18.000 (3 métricas × 250 gen × 3 runs × 2 alg × 2 prob)
- **Gráficos gerados**: 8 (4 PNG + 4 PDF)

---

## 📧 Suporte

Para questões sobre:

- **Compilação LaTeX**: Consulte documentação TeX Live/MiKTeX
- **Conteúdo científico**: Revise seções individuais em `sections/`
- **Dados experimentais**: Consulte `../CONVERGENCE_README.md`
- **Gráficos**: Consulte `../PLOTS_README.md`

---

## 📜 Licença

Este documento é parte do projeto **OCEV - Otimização com Convergência Evolutiva**.

Código-fonte e dados disponíveis em: https://github.com/AmonOnly/Ocev_MOEA

---

## ✅ Checklist de Compilação

Antes de compilar, verifique:

- [ ] Distribuição LaTeX instalada (TeX Live/MiKTeX)
- [ ] Pasta `../plots/` contém todos os 8 PDFs dos gráficos
- [ ] Arquivo `main.tex` está acessível
- [ ] Pasta `sections/` contém todos os 10 arquivos `.tex`
- [ ] Compilador configurado para **pdfLaTeX**
- [ ] Executar compilação **2 vezes** para resolver referências

---

**Última atualização**: 26 de outubro de 2025

**Versão do documento**: 1.0
