import plotly.express as px
import streamlit as st
import pandas as pd

# ==============================
# CORES PADRÃO
# ==============================

CORES = {
    "ST_SOLICITADO": "#1f77b4",  # azul
    "ST_AVALIADO": "#2ca02c",    # verde
    "QT_EXM": "#ff7f0e",         # laranja
    "QT_PRC": "#d62728",         # vermelho
    "PCT_AVALIADO": "#9467bd"    # roxo (novo indicador)
}

# ==============================
# FUNÇÃO PRINCIPAL
# ==============================

def render_charts(df):

    # ==============================
    # PREPARAÇÃO DO TEMPO
    # ==============================

    df["COMPETENCIA_DT"] = pd.to_datetime(df["COMPETENCIA"], format="%Y%m")

    df_group = (
        df
        .groupby(["COMPETENCIA", "COMPETENCIA_DT"])
        .sum(numeric_only=True)
        .reset_index()
        .sort_values("COMPETENCIA_DT")
    )

    # ordem correta do eixo X
    ordem = df_group["COMPETENCIA"].tolist()

    # ==============================
    # FUNÇÃO AUXILIAR
    # ==============================

    def gerar_grafico(coluna, titulo, cor):

        fig = px.line(
            df_group,
            x="COMPETENCIA",
            y=coluna,
            title=titulo,
            category_orders={"COMPETENCIA": ordem},
            markers=True
        )

        fig.update_traces(line=dict(color=cor))

        fig.update_layout(
            xaxis_title="Competência",
            yaxis_title="Valor",
            xaxis=dict(type="category")
        )

        return fig

    # ==============================
    # GRÁFICOS PRINCIPAIS
    # ==============================

    st.plotly_chart(
        gerar_grafico("ST_SOLICITADO", "Exames Solicitados", CORES["ST_SOLICITADO"]),
        width="stretch"
    )

    st.plotly_chart(
        gerar_grafico("ST_AVALIADO", "Exames Avaliados", CORES["ST_AVALIADO"]),
        width="stretch"
    )

    st.plotly_chart(
        gerar_grafico("QT_EXM", "Quantidade de Exames", CORES["QT_EXM"]),
        width="stretch"
    )

    st.plotly_chart(
        gerar_grafico("QT_PRC", "Procedimentos", CORES["QT_PRC"]),
        width="stretch"
    )

    # ==============================
    # NOVO INDICADOR (%)
    # ==============================

    df_group["PCT_AVALIADO"] = (
        df_group["ST_AVALIADO"] / df_group["ST_SOLICITADO"]
    ).replace([float("inf"), -float("inf")], 0).fillna(0)

    fig_pct = px.line(
        df_group,
        x="COMPETENCIA",
        y="PCT_AVALIADO",
        title="% Exames Avaliados",
        category_orders={"COMPETENCIA": ordem},
        markers=True
    )

    fig_pct.update_traces(line=dict(color=CORES["PCT_AVALIADO"]))

    fig_pct.update_layout(
        xaxis_title="Competência",
        yaxis_title="Percentual",
        xaxis=dict(type="category"),
        yaxis_tickformat=".0%"
    )

    st.plotly_chart(fig_pct, width="stretch")