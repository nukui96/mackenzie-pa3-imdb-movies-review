# Base de dados

`raw/imdb_top_1000.csv` foi obtido em setembro de 2026 da página [IMDB Dataset of Top 1000 Movies and TV Shows](https://www.kaggle.com/datasets/harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows), publicada por Harshit Shankhdhar no Kaggle. A página apresenta o dataset como [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Essa indicação do mantenedor não esclarece, por si só, os direitos sobre dados originalmente atribuídos ao IMDb. O CSV bruto é mantido sem alterações: 1.000 registros e 16 colunas.

`processed/filmes_preparados.csv` é gerado pelo notebook `02_exploracao-e-preparacao.ipynb`. As regras de preparação e a reconciliação com o arquivo bruto estão em [`../docs/tratamento_base_dados.md`](../docs/tratamento_base_dados.md).
