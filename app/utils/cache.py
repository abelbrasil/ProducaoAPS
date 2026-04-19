import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

@st.cache_resource
def get_engine():
    return create_engine(os.getenv("DATABASE_URL"), pool_pre_ping=True)

@st.cache_data(ttl=600)
def run_query(query):
    engine = get_engine()
    return pd.read_sql(query, engine)