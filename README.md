# Projeto Aplicado III: recomendação de filmes por conteúdo

Projeto desenvolvido por Kayo Oliveira Nukui (TIA 10356420), no curso de Tecnologia em Banco de Dados da Universidade Presbiteriana Mackenzie.

## Objetivo

Criar uma primeira versão de um recomendador que, a partir de um filme escolhido, mostre cinco títulos com sinopses semelhantes. Os arquivos deste repositório correspondem às etapas 1 e 2.

## Base

[IMDB Dataset of Top 1000 Movies and TV Shows](https://www.kaggle.com/datasets/harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows), publicada por Harshit Shankhdhar no Kaggle e obtida em setembro de 2026. O arquivo contém 1.000 títulos e 16 colunas, sem identificação de usuários nem histórico de interações. Por isso, o projeto usa recomendação por conteúdo. Detalhes em [`data/README.md`](data/README.md).

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `entregas/` | Relatórios em PDF, organizados por etapa. |
| `notebooks/` | Notebooks 01 (dados e qualidade), 02 (exploração e preparação) e 03 (prova de conceito). Ver [`notebooks/README.md`](notebooks/README.md). |
| `src/` | Funções importadas pelos notebooks: inspeção, preparação e recomendação. Ver [`src/README.md`](src/README.md). |
| `data/raw/`, `data/processed/` | CSV bruto e catálogo preparado gerado pelo notebook 02. |
| `reports/figures/`, `reports/metrics/` | Figuras e métricas geradas pelos notebooks 02 e 03. |
| `docs/` | Ambiente de execução e regras de tratamento da base. |

## Execução

Na raiz do projeto, crie um ambiente virtual:

```bash
python -m venv .venv
```

Após ativá-lo, execute `python -m pip install -r requirements.txt`. Abra os notebooks em um ambiente Jupyter e use **Restart & Run All** na ordem 01, 02, 03; o 03 lê o arquivo gerado pelo 02. As versões das bibliotecas e a situação da execução estão em [`docs/ambiente.md`](docs/ambiente.md).

## Método e resultado preliminar

O modelo usa TF-IDF para representar as palavras das sinopses (`Overview`) e similaridade do cosseno para ordenar os filmes. O gênero não entra no cálculo das recomendações. Comparamos a lista de cinco títulos com duas referências simples: os filmes mais votados e uma lista sorteada. Como a base não contém opiniões individuais sobre essas sugestões, contamos quantos filmes recomendados compartilham algum gênero com o filme escolhido. Essa medida é apenas um **indicador indireto**, chamado de proxy. Os números estão em [`reports/metrics/metricas_poc.csv`](reports/metrics/metricas_poc.csv).

## Limites

- Compartilhar um gênero não significa que a pessoa gostará do filme. A medida é permissiva porque Drama aparece em 72,4% do catálogo.
- A base contém apenas os 1.000 títulos mais bem avaliados do IMDb, com sinopses curtas em inglês.
- Esta prova de conceito não inclui ajuste de parâmetros, avaliação com usuários ou aplicação junto à comunidade.
- A página do dataset no Kaggle indica CC0 1.0. Essa indicação do mantenedor não esclarece, por si só, os direitos sobre dados originalmente atribuídos ao IMDb.
