# Ambiente de execução

As dependências do projeto estão fixadas em `requirements.txt`.

## Bibliotecas utilizadas

| Biblioteca | Uso nesta etapa |
|---|---|
| `pandas` | Ler os CSVs, conferir a base e preparar as colunas. |
| `numpy` | Organizar os cálculos dos rankings e das métricas. |
| `matplotlib` | Produzir os gráficos da análise exploratória e da prova de conceito. |
| `scikit-learn` | Ajustar o TF-IDF às sinopses e calcular a similaridade do cosseno. |
| `nbclient`, `nbformat` e `ipykernel` | Executar e verificar os notebooks em ambiente Jupyter. |

O ajuste do TF-IDF aprende o vocabulário e os pesos dos termos a partir das sinopses do catálogo. Como não há avaliações de usuários na base, esta prova de conceito não treina um modelo supervisionado para prever preferências individuais.

Para reproduzir, crie e ative um ambiente virtual na raiz do projeto e instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

Execute os notebooks `01`, `02` e `03` nessa ordem. O notebook 03 lê `data/processed/filmes_preparados.csv`, gerado pelo 02. Os notebooks encontram a raiz do projeto pelo arquivo `data/raw/imdb_top_1000.csv`.
