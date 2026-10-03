"""Prova de conceito: recomendação por conteúdo (TF-IDF sobre Overview) e linhas de base.

O gênero NÃO entra no modelo. É usado somente na avaliação proxy.
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

K = 5


def matriz_similaridade(textos):
    """TF-IDF (stop words em inglês, demais parâmetros padrão) e similaridade de cosseno."""
    vetor = TfidfVectorizer(stop_words="english")
    X = vetor.fit_transform(textos)
    return X, cosine_similarity(X), vetor


def ranking_conteudo(sim, ano, i, k=K):
    """Top-k por similaridade; exclui a consulta; desempate por ano (NA por último) e film_id."""
    ids = np.arange(sim.shape[0])
    ano_ord = np.where(pd.isna(ano), np.inf, np.asarray(pd.Series(ano).fillna(0), dtype=float))
    ordem = np.lexsort((ids, ano_ord, -sim[i]))
    return [j for j in ordem if j != i][:k]


def ranking_popularidade(votos, i, k=K):
    """Mais votados do catálogo, exceto a consulta; desempate por film_id."""
    ids = np.arange(len(votos))
    ordem = np.lexsort((ids, -np.asarray(votos)))
    return [j for j in ordem if j != i][:k]


def ranking_aleatorio(n, i, rng, k=K):
    """k filmes sorteados sem reposição entre os demais (n-1 candidatos)."""
    candidatos = np.delete(np.arange(n), i)
    return list(rng.choice(candidatos, size=k, replace=False))


def conjunto_generos(serie_genero):
    return [set(g.split(", ")) for g in serie_genero]


def metricas_proxy(generos, i, recs):
    """Proxy: fração das recs que compartilham >=1 gênero com a consulta, e Jaccard médio."""
    q = generos[i]
    comp = [len(q & generos[j]) > 0 for j in recs]
    jac = [len(q & generos[j]) / len(q | generos[j]) for j in recs]
    return float(np.mean(comp)), float(np.mean(jac))


## RA: 10356420 - KAYO OLIVEIRA NUKUI ##