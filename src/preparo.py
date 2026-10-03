"""Regras de preparação do catálogo IMDb Top 1000 (etapa 2).

O CSV bruto nunca é alterado: a função devolve um novo DataFrame.
Valor ausente permanece ausente (NA); nunca é convertido em zero.
"""

import pandas as pd

COLUNAS_SAIDA = [
    "film_id", "Series_Title", "Released_Year", "Certificate", "Runtime_min",
    "Genre", "IMDB_Rating", "Meta_score", "No_of_Votes", "Gross_usd",
    "Director", "Star1", "Star2", "Star3", "Star4", "Overview",
    "Overview_chars", "Overview_words",
]


def preparar_catalogo(bruto: pd.DataFrame) -> pd.DataFrame:
    """Aplica as regras R1-R7 descritas em docs/tratamento_base_dados.md."""
    df = bruto.copy()
    # R1: identificador estável = posição (0-based) da linha no CSV bruto.
    df.insert(0, "film_id", range(len(df)))
    # R2: texto sem espaços nas pontas e com espaços internos colapsados.
    for col in ["Series_Title", "Overview", "Genre", "Director", "Star1", "Star2", "Star3", "Star4"]:
        df[col] = df[col].astype("string").str.strip().str.replace(r"\s+", " ", regex=True)
    # R3: ano numérico; valor não numérico (ex.: "PG") vira NA, sem imputação externa.
    df["Released_Year"] = pd.to_numeric(df["Released_Year"], errors="coerce").astype("Int64")
    # R4: duração "142 min" -> inteiro em minutos.
    df["Runtime_min"] = pd.to_numeric(df["Runtime"].str.extract(r"^(\d+) min$")[0], errors="coerce").astype("Int64")
    # R5: bilheteria "28,341,469" -> inteiro em dólares; ausente permanece NA (não é zero).
    df["Gross_usd"] = pd.to_numeric(df["Gross"].str.replace(",", "", regex=False), errors="coerce").astype("Int64")
    # R6: Certificate e Meta_score ausentes permanecem NA (sem preenchimento).
    df["Certificate"] = df["Certificate"].astype("string")
    df["Meta_score"] = df["Meta_score"].astype("Float64")
    # R7: medidas de tamanho da sinopse (apenas descritivas).
    df["Overview_chars"] = df["Overview"].str.len().astype("Int64")
    df["Overview_words"] = df["Overview"].str.split().str.len().astype("Int64")
    return df[COLUNAS_SAIDA]

## RA: 10356420 - KAYO OLIVEIRA NUKUI ##