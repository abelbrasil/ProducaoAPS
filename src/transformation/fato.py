import pandas as pd

def criar_fato(df_exames, df_procedimentos):
    df_exames_fato = df_exames.rename(columns={"CO_EXAME": "CO_PROCEDIMENTO"})
    df_base = pd.concat([df_exames_fato, df_procedimentos], ignore_index=True)

    fato = (
        df_base
        .groupby(["COMPETENCIA", "CO_MUNICIPIO_IBGE", "CO_PROCEDIMENTO"], as_index=False)
        .agg({
            "ST_SOLICITADO": "sum",
            "ST_AVALIADO": "sum",
            "QT_EXM": "sum",
            "QT_PRC": "sum"
        })
    )

    return fato