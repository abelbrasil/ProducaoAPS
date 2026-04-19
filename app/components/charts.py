import plotly.express as px
import streamlit as st
import pandas as pd

CORES = {
    "ST_SOLICITADO": "#1f77b4",
    "ST_AVALIADO": "#2ca02c",
    "QT_EXM": "#ff7f0e",
    "QT_PRC": "#d62728"
}

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

    # garantir categoria ordenada
    ordem = df_group["COMPETENCIA"].tolist()

    # ==============================
    # GRÁFICOS
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
            xaxis=dict(type="category")  # 🔥 força categórico
        )

        return fig

    st.plotly_chart(
        gerar_grafico("ST_SOLICITADO", "Exames Solicitados", CORES["ST_SOLICITADO"]),
        use_container_width=True
    )

    st.plotly_chart(
        gerar_grafico("ST_AVALIADO", "Exames Avaliados", CORES["ST_AVALIADO"]),
        use_container_width=True
    )

    st.plotly_chart(
        gerar_grafico("QT_EXM", "Quantidade de Exames", CORES["QT_EXM"]),
        use_container_width=True
    )

    st.plotly_chart(
        gerar_grafico("QT_PRC", "Procedimentos", CORES["QT_PRC"]),
        use_container_width=True
    )