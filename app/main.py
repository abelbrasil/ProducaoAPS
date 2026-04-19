import streamlit as st
from utils.cache import run_query
from services.queries import get_base_query

from components.cards import render_cards
from components.charts import render_charts
from components.tables import render_tables

# ==============================
# CONFIG
# ==============================

st.set_page_config(page_title="Painel APS", layout="wide")
st.title("📊 Painel de Produção APS")

# ==============================
# LOAD
# ==============================

df_base = run_query(get_base_query())

# garantir tipo
df_base["COMPETENCIA"] = df_base["COMPETENCIA"].astype(str)
df_base["ANO"] = df_base["COMPETENCIA"].str[:4]

## ==============================
# FILTROS
# ==============================

st.sidebar.header("🎛️ Filtros")

# ------------------------------
# ANO
# ------------------------------
anos = sorted(df_base["ANO"].unique())

anos_sel = st.sidebar.multiselect(
    "Ano",
    anos
)

# base auxiliar para período (dependente do ano)
df_ano = df_base.copy()

if anos_sel:
    df_ano = df_ano[df_ano["ANO"].isin(anos_sel)]

# ------------------------------
# PERÍODO
# ------------------------------
periodos = sorted(df_ano["COMPETENCIA"].unique())

periodos_sel = st.sidebar.multiselect(
    "Período",
    periodos
)

# ------------------------------
# MUNICÍPIO
# ------------------------------
municipios = sorted(df_base["NO_MUNICIPIO"].dropna().unique())

mun_sel = st.sidebar.multiselect(
    "Município",
    municipios
)

# ------------------------------
# EXAME
# ------------------------------
exames = sorted(df_base["EXAME"].dropna().unique())

ex_sel = st.sidebar.multiselect(
    "Exame",
    exames
)

# ==============================
# APLICAÇÃO FINAL DOS FILTROS
# ==============================

df = df_base.copy()

# aplicar só se tiver seleção

if anos_sel:
    df = df[df["ANO"].isin(anos_sel)]

if periodos_sel:
    df = df[df["COMPETENCIA"].isin(periodos_sel)]

if mun_sel:
    df = df[df["NO_MUNICIPIO"].isin(mun_sel)]

if ex_sel:
    df = df[df["EXAME"].isin(ex_sel)]

# ==============================
# VALIDAÇÃO
# ==============================

if df.empty:
    st.warning("⚠️ Nenhum dado encontrado com os filtros selecionados.")
    st.stop()

# ==============================
# DASHBOARD
# ==============================

render_cards(df)

st.divider()

st.subheader("📈 Evolução Temporal")
render_charts(df)

st.divider()

render_tables(df)

# ==============================
# FOOTER
# ==============================

st.divider()
st.caption("Fonte: Produção APS | Pipeline Python + Supabase")