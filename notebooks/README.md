# Notebooks

Os notebooks numerados separam inspeção dos dados, preparação e prova de conceito. Execute-os na ordem indicada; veja o ambiente em `../docs/ambiente.md`.

| Notebook | Conteúdo |
|---|---|
| `01_dados-e-qualidade.ipynb` | Origem, esquema, nulos, tipos e unicidade do CSV bruto. |
| `02_exploracao-e-preparacao.ipynb` | Análise exploratória, regras de preparação e geração de `data/processed/filmes_preparados.csv`. |
| `03_modelo-inicial.ipynb` | TF-IDF sobre a sinopse, Top 5, linhas de base e avaliação indireta por gênero. |

Ordem de execução: 01, 02, 03 (o 03 lê o arquivo gerado pelo 02). Cada notebook localiza a raiz subindo pelas pastas até achar `data/raw/imdb_top_1000.csv`; pode ser aberto a partir de `notebooks/` ou da raiz.

Saídas geradas: `../data/processed/`, `../reports/figures/` e `../reports/metrics/`. A avaliação do notebook 03 usa um proxy indireto (sobreposição de gêneros) e não mede relevância para usuários.
