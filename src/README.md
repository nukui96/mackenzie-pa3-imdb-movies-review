# Rotinas do PA3

| Módulo | Função |
|---|---|
| `inspect_data.py` | Inspeção inicial do CSV bruto: exige colunas, conta registros, células vazias e duplicatas exatas. Não altera dados. |
| `preparo.py` | `preparar_catalogo`: regras R1 a R7 de preparação (ver `../docs/tratamento_base_dados.md`). Devolve um novo DataFrame; o bruto não é modificado. |
| `recomendador.py` | TF-IDF sobre a sinopse, similaridade de cosseno, rankings Top 5 (conteúdo, popularidade, aleatório) e métricas proxy por gênero. O gênero não entra no modelo, só na avaliação. |

Uso de `inspect_data.py`, da raiz do projeto:

```powershell
python src/inspect_data.py data/raw/imdb_top_1000.csv --required Series_Title Overview Genre
```

`preparo.py` e `recomendador.py` são importados pelos notebooks 02 e 03. Nenhum módulo mede a validade das recomendações para usuários.
