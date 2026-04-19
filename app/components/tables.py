import streamlit as st

def render_tables(df):

    tabela = (
        df.groupby("EXAME")[["ST_SOLICITADO","ST_AVALIADO","QT_EXM","QT_PRC"]]
        .sum()
        .sort_index()
        .reset_index()
    )

    st.subheader("📋 Produção por Exame")
    st.dataframe(tabela, use_container_width=True)

    top10 = tabela.sort_values("QT_EXM", ascending=False).head(10)

    st.subheader("🏆 Top 10 Exames")
    st.dataframe(top10, use_container_width=True)