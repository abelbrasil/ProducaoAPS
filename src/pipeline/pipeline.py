import pandas as pd

from src.utils.helpers import padronizar_codigo
from src.ingestion.ibge import get_ibge_municipios

from src.transformation.fato import criar_fato
from src.transformation.dim_procedimentos import criar_dim_procedimentos
from src.transformation.dim_calendario import criar_dim_calendario
from src.transformation.dim_municipio import criar_dim_municipio


def executar_pipeline():

    df_exames = pd.read_excel("./data/exames_fortaleza.xlsx")
    df_procedimentos = pd.read_excel("./data/procedimentos.xlsx")

    df_exames["CO_EXAME"] = padronizar_codigo(df_exames, "CO_EXAME")
    df_procedimentos["CO_PROCEDIMENTO"] = padronizar_codigo(df_procedimentos, "CO_PROCEDIMENTO")

    fato = criar_fato(df_exames, df_procedimentos)

    dim_proc = criar_dim_procedimentos(df_exames, df_procedimentos)
    dim_cal = criar_dim_calendario(fato)

    df_ibge = get_ibge_municipios()
    dim_mun = criar_dim_municipio(fato, df_ibge)

    return fato, dim_proc, dim_cal, dim_mun