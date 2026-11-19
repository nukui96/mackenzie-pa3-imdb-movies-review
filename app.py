"""Interface Streamlit para consulta ao recomendador IMDb Top 1000."""

import logging
from pathlib import Path
import sys

import numpy as np
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from recomendador import K, matriz_similaridade, ranking_conteudo

CSV_PROCESSADO = ROOT / "data" / "processed" / "filmes_preparados.csv"
logger = logging.getLogger(__name__)


def formatar_rotulo(titulo, ano) -> str:
    if pd.isna(ano):
        return f"{titulo} (Ano não informado)"
    return f"{titulo} ({int(ano)})"


@st.cache_resource
def carregar_dados_e_modelo():
    if not CSV_PROCESSADO.is_file():
        raise FileNotFoundError(f"Arquivo ausente: {CSV_PROCESSADO}")

    df = pd.read_csv(CSV_PROCESSADO)
    df["Released_Year"] = pd.to_numeric(df["Released_Year"], errors="coerce").astype("Int64")

    ids_esperados = np.arange(len(df))
    if len(df) == 0 or not np.array_equal(df["film_id"].to_numpy(), ids_esperados):
        raise ValueError("Identificador film_id fora de alinhamento com as posições da matriz.")

    _, sim, _ = matriz_similaridade(df["Overview"].fillna(""))

    rotulos = {
        int(row.film_id): formatar_rotulo(row.Series_Title, row.Released_Year)
        for row in df.itertuples(index=False)
    }
    opcoes_ids = sorted(rotulos.keys(), key=lambda fid: rotulos[fid].casefold())
    return df, sim, rotulos, opcoes_ids


def main():
    st.set_page_config(page_title="Recomendador de Filmes", layout="centered")
    st.title("Recomendador de Filmes")
    st.write("Escolha um filme do catálogo IMDb Top 1000 e descubra cinco títulos com sinopses semelhantes.")

    try:
        df, sim, rotulos, opcoes_ids = carregar_dados_e_modelo()
    except FileNotFoundError:
        logger.exception("Catálogo processado não encontrado em %s", CSV_PROCESSADO)
        st.error("O arquivo do catálogo preparado não foi encontrado. Execute a etapa de preparação dos dados antes de abrir a interface.")
        return
    except Exception:
        logger.exception("Falha ao carregar o catálogo ou inicializar a matriz de similaridade.")
        st.error("Não foi possível carregar o catálogo de filmes no momento.")
        return

    film_id_selecionado = st.selectbox(
        label="Pesquise um filme pelo título",
        options=opcoes_ids,
        index=None,
        format_func=lambda fid: rotulos[fid],
        placeholder="Digite parte do nome para encontrar o filme desejado.",
    )

    if st.button("Encontrar filmes semelhantes"):
        if film_id_selecionado is None:
            st.session_state["id_consultado"] = None
            st.info("Selecione um filme para continuar.")
        else:
            st.session_state["id_consultado"] = int(film_id_selecionado)

    id_ativo = st.session_state.get("id_consultado")
    if id_ativo is None or id_ativo != film_id_selecionado:
        return

    ancora = df.iloc[id_ativo]
    rotulo_ancora = rotulos[id_ativo]
    recs_ids = ranking_conteudo(sim, df["Released_Year"], id_ativo, k=K)

    st.divider()
    st.subheader("Filme selecionado")
    st.markdown(f"**{rotulo_ancora}**")
    st.write(f"**Gêneros:** {ancora['Genre']}")
    st.write(f"**Sinopse:** {ancora['Overview']}")

    st.divider()
    st.subheader(f"Filmes semelhantes a {rotulo_ancora}")
    st.caption(
        "As recomendações são calculadas a partir da semelhança entre as sinopses. "
        "Isso não significa que os filmes tenham histórias iguais."
    )

    for pos, rec_id in enumerate(recs_ids, start=1):
        rec = df.iloc[rec_id]
        score = float(sim[id_ativo, rec_id])
        st.markdown(f"**{pos}º. {rotulos[rec_id]}**")
        st.write(f"Gêneros: {rec['Genre']} | Similaridade do cosseno: `{score:.4f}`")
        with st.expander("Ver sinopse"):
            st.write(rec["Overview"])


if __name__ == "__main__":
    main()
