import streamlit as st

def render_cards(df):

    # ==============================
    # AGREGAÇÃO
    # ==============================

    total_solicitado = df["ST_SOLICITADO"].sum()
    total_avaliado = df["ST_AVALIADO"].sum()
    total_exames = df["QT_EXM"].sum()
    total_proc = df["QT_PRC"].sum()

    qtd_comp = df["COMPETENCIA"].nunique() or 1

    # médias
    media_solicitado = total_solicitado / qtd_comp
    media_avaliado = total_avaliado / qtd_comp
    media_exames = total_exames / qtd_comp
    media_proc = total_proc / qtd_comp

    # ==============================
    # NOVO INDICADOR (%)
    # ==============================

    pct_avaliado = 0
    if total_solicitado > 0:
        pct_avaliado = total_avaliado / total_solicitado

    # ==============================
    # CARDS TOTAIS
    # ==============================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📘 Exames Solicitados", f"{total_solicitado:,.0f}")
    col2.metric("📗 Exames Avaliados", f"{total_avaliado:,.0f}")
    col3.metric("📙 Quantidade de Exames", f"{total_exames:,.0f}")
    col4.metric("📕 Procedimentos", f"{total_proc:,.0f}")

    # ==============================
    # CARDS MÉDIAS
    # ==============================

    col5, col6, col7, col8 = st.columns(4)

    col5.metric("📘 Média Exames Solicitados", f"{media_solicitado:,.0f}")
    col6.metric("📗 Média Exames Avaliados", f"{media_avaliado:,.0f}")
    col7.metric("📙 Média Quantidade de Exames", f"{media_exames:,.0f}")
    col8.metric("📕 Média Procedimentos", f"{media_proc:,.0f}")

    # ==============================
    # NOVO CARD (%)
    # ==============================

    col_pct, _ = st.columns([1, 3])

    col_pct.metric(
        "📊 % Exames Avaliados",
        f"{pct_avaliado:.2%}"
    )