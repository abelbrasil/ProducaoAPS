import streamlit as st

def render_cards(df):

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📘 Exames Solicitados", f"{df['ST_SOLICITADO'].sum():,.0f}")
    col2.metric("📗 Exames Avaliados", f"{df['ST_AVALIADO'].sum():,.0f}")
    col3.metric("📙 Quantidade de Exames", f"{df['QT_EXM'].sum():,.0f}")
    col4.metric("📕 Procedimentos", f"{df['QT_PRC'].sum():,.0f}")