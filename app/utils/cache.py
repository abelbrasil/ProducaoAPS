import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# ==============================
# LOAD .env (LOCAL)
# ==============================

load_dotenv()

# ==============================
# FUNÇÃO DE CONEXÃO
# ==============================

@st.cache_resource
def get_engine():

    # prioridade: .env (local) → secrets (cloud)
    db_url = os.getenv("DATABASE_URL")

    if not db_url:
        try:
            db_url = st.secrets["DATABASE_URL"]
        except Exception:
            raise ValueError("DATABASE_URL não encontrada (.env ou secrets.toml)")

    return create_engine(
        db_url,
        pool_pre_ping=True
    )

# ==============================
# EXECUÇÃO DE QUERY COM CACHE
# ==============================

@st.cache_data(ttl=600)
def run_query(query):

    engine = get_engine()

    return pd.read_sql(query, engine)