from src.database.connection import engine
from src.database.models import Base

def criar_banco():
    Base.metadata.create_all(bind=engine)


def carregar_dataframe(df, tabela_nome):
    df.to_sql(
        tabela_nome,
        con=engine,
        if_exists="replace",
        index=False
    )