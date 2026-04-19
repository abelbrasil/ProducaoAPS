import pandas as pd
from sqlalchemy import create_engine

def test_soma_metricas_fato_sqlite():

    engine = create_engine("sqlite:///./db/aps.db")

    fato = pd.read_sql("SELECT * FROM fato_prod_aps", engine)

    df_exames = pd.read_excel("./data/exames_fortaleza.xlsx")
    df_procedimentos = pd.read_excel("./data/procedimentos.xlsx")

    # origem
    soma_origem = {
        "ST_SOLICITADO": df_exames["ST_SOLICITADO"].sum(),
        "ST_AVALIADO": df_exames["ST_AVALIADO"].sum(),
        "QT_EXM": df_exames["QT_EXM"].sum(),
        "QT_PRC": df_procedimentos["QT_PRC"].sum()
    }

    # fato
    soma_fato = fato[["ST_SOLICITADO","ST_AVALIADO","QT_EXM","QT_PRC"]].sum().to_dict()

    # 🔥 PRINT NA TELA
    print("\n===== COMPARAÇÃO DE MÉTRICAS =====")
    for col in soma_origem.keys():
        print(f"{col}: ORIGEM = {soma_origem[col]} | FATO = {soma_fato[col]}")

    # validação
    for col in soma_origem.keys():
        assert round(soma_origem[col], 5) == round(soma_fato[col], 5)