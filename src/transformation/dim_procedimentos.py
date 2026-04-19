import pandas as pd

def criar_dim_procedimentos(df_exames, df_procedimentos):
    df_dim_exames = df_exames[["CO_EXAME", "EXAME"]].copy()

    df_dim_proc = df_procedimentos[["CO_PROCEDIMENTO", "PROCEDIMENTO"]].copy()
    df_dim_proc.columns = ["CO_EXAME", "EXAME"]

    dim = pd.concat([df_dim_exames, df_dim_proc], ignore_index=True)

    # remover duplicados exatos
    dim["FL_DUPLICADO"] = dim.duplicated(["CO_EXAME", "EXAME"], keep="first")
    dim = dim[~dim["FL_DUPLICADO"]]

    # flags iniciais
    dim["FL_DUPLI_CO"] = dim.duplicated(["CO_EXAME"], keep=False)
    dim["FL_DUPLI_NM"] = dim.duplicated(["EXAME"], keep=False)

    # inconsistência
    map_inconsistencia = (
        dim.groupby("CO_EXAME")["EXAME"].nunique().gt(1)
    )
    dim["FL_INCONSISTENTE"] = dim["CO_EXAME"].map(map_inconsistencia)

    # tratamento de missing
    dim["FL_NOME_VAZIO"] = dim["EXAME"].isna() | (dim["EXAME"].str.strip() == "")

    codigos_validos = dim.groupby("CO_EXAME")["FL_NOME_VAZIO"].apply(lambda x: (~x).any())
    dim["FL_TEM_NOME_VALIDO"] = dim["CO_EXAME"].map(codigos_validos)

    dim = dim[~((dim["FL_NOME_VAZIO"]) & (dim["FL_TEM_NOME_VALIDO"]))]

    dim["FL_SEM_DESCRICAO"] = dim.groupby("CO_EXAME")["FL_NOME_VAZIO"].transform(lambda x: x.all())

    dim = dim.drop(columns=["FL_NOME_VAZIO", "FL_TEM_NOME_VALIDO"])

    # recalcular flags
    dim["FL_DUPLICADO"] = dim.duplicated(["CO_EXAME", "EXAME"], keep="first")
    dim["FL_DUPLI_CO"] = dim.duplicated(["CO_EXAME"], keep=False)
    dim["FL_DUPLI_NM"] = dim.duplicated(["EXAME"], keep=False)

    map_inconsistencia = dim.groupby("CO_EXAME")["EXAME"].nunique().gt(1)
    dim["FL_INCONSISTENTE"] = dim["CO_EXAME"].map(map_inconsistencia)

    dim["TP_CODIGO"] = dim["CO_EXAME"].str.len()

    return dim.sort_values("CO_EXAME").reset_index(drop=True)