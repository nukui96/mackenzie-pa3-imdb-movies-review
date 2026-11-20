# Projeto Aplicado III: recomendação de filmes por conteúdo

Projeto desenvolvido por Kayo Oliveira Nukui (TIA 10356420), no curso de Tecnologia em Banco de Dados da Universidade Presbiteriana Mackenzie.

## Objetivo

Criar e avaliar um recomendador reproduzível que, a partir de um filme escolhido no catálogo, mostre cinco títulos com sinopses semelhantes.

## Base

[IMDB Dataset of Top 1000 Movies and TV Shows](https://www.kaggle.com/datasets/harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows), publicada por Harshit Shankhdhar no Kaggle e obtida em setembro de 2026. O arquivo contém 1.000 títulos e 16 colunas, sem identificação de usuários nem histórico de interações. Por isso, o projeto usa recomendação por conteúdo. Detalhes em [`data/README.md`](data/README.md).

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `app.py` | Interface Streamlit para consulta de recomendações. |
| `entregas/` | Relatórios em PDF, organizados por etapa. |
| `notebooks/` | Notebooks 01 (dados e qualidade), 02 (exploração e preparação) e 03 (prova de conceito e avaliação). Ver [`notebooks/README.md`](notebooks/README.md). |
| `src/` | Funções de inspeção, preparação e recomendação usadas pelos notebooks e pelo aplicativo. Ver [`src/README.md`](src/README.md). |
| `data/raw/`, `data/processed/` | CSV bruto e catálogo preparado gerado pelo notebook 02. |
| `reports/figures/`, `reports/metrics/` | Figuras e métricas geradas pelos notebooks 02 e 03 e fluxograma da metodologia. |
| `docs/` | Ambiente de execução e regras de tratamento da base. |

## Execução

Na raiz do projeto, crie e ative um ambiente virtual e instale as dependências:

```bash
python -m venv .venv
python -m pip install -r requirements.txt
```

Para reproduzir as análises, execute os notebooks em Jupyter na ordem `01`, `02`, `03` (**Restart & Run All**), pois o `03` lê o catálogo gerado pelo `02`. Para abrir a interface interativa usando o catálogo já preparado, execute:

```bash
streamlit run app.py
```

Detalhes do ambiente estão em [`docs/ambiente.md`](docs/ambiente.md).

## Método e resultado

O recomendador representa as sinopses (`Overview`) com TF-IDF e ordena os títulos por similaridade do cosseno. O gênero não entra no cálculo das recomendações. Como a base não tem avaliações de usuários, a avaliação offline compara o Top 5 gerado com duas linhas de base (filmes mais votados e sorteio aleatório) usando:

- coincidência de gêneros com a consulta (indicador indireto, chamado de proxy);
- proximidade média de cosseno com o filme consultado;
- diversidade de gêneros dentro do Top 5 (1 - Jaccard entre os dez pares recomendados);
- cobertura agregada do catálogo.

Os resultados estão em [`reports/metrics/metricas_poc.csv`](reports/metrics/metricas_poc.csv).

## Limites

- Compartilhar um gênero não significa que a pessoa gostará do filme. A medida é permissiva porque Drama aparece em 72,4% do catálogo.
- A base contém apenas os 1.000 títulos mais bem avaliados do IMDb, com sinopses curtas em inglês.
- Esta prova de conceito não inclui ajuste de parâmetros, avaliação com usuários ou aplicação junto à comunidade.
- A página do dataset no Kaggle indica CC0 1.0. Essa indicação do mantenedor não esclarece, por si só, os direitos sobre dados originalmente atribuídos ao IMDb.
