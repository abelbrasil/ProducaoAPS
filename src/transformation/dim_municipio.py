def criar_dim_municipio(fato, df_ibge):

    # base
    dim = fato[["CO_MUNICIPIO_IBGE"]].drop_duplicates().copy()

    dim["CO_MUNICIPIO_IBGE"] = dim["CO_MUNICIPIO_IBGE"].astype(str)

    # chave auxiliar (6 dígitos)
    dim["CO_MUN_6"] = dim["CO_MUNICIPIO_IBGE"].str.zfill(6)
    df_ibge["CO_MUNICIPIO_IBGE"] = df_ibge["CO_MUNICIPIO_IBGE"].astype(str)
    df_ibge["CO_MUN_6"] = df_ibge["CO_MUNICIPIO_IBGE"].str[:6]

    # merge
    dim = dim.merge(
        df_ibge,
        on="CO_MUN_6",
        how="left"
    )

    # 🔴 CORREÇÃO CRÍTICA: restaurar coluna original
    dim["CO_MUNICIPIO_IBGE"] = dim["CO_MUNICIPIO_IBGE_x"]

    # remover colunas auxiliares
    dim = dim.drop(columns=[
        "CO_MUN_6",
        "CO_MUNICIPIO_IBGE_x",
        "CO_MUNICIPIO_IBGE_y"
    ])

    # flag
    dim["FL_NAO_ENCONTRADO"] = dim["NO_MUNICIPIO"].isna()

    dim = dim[[
        "CO_MUNICIPIO_IBGE",
        "NO_MUNICIPIO",
        "UF",
        "NO_UF",
        "REGIAO",
        "FL_NAO_ENCONTRADO"
    ]]

    return dim.sort_values("CO_MUNICIPIO_IBGE").reset_index(drop=True)