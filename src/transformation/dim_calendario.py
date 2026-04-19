import pandas as pd

def criar_dim_calendario(fato):

    fato["COMPETENCIA"] = fato["COMPETENCIA"].astype(str)

    periodo_min = fato["COMPETENCIA"].min()
    periodo_max = fato["COMPETENCIA"].max()

    # criar Period (mantém tipo correto)
    dim = pd.DataFrame({
        "PERIODO": pd.period_range(start=periodo_min, end=periodo_max, freq="M")
    })

    # 🔴 EXTRAIR ANTES DE CONVERTER
    dim["ANO"] = dim["PERIODO"].dt.year
    dim["MES"] = dim["PERIODO"].dt.month

    # nomes dos meses
    map_meses = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }

    dim["NOME_MES"] = dim["MES"].map(map_meses)

    # derivados
    dim["ANO_MES"] = dim["ANO"].astype(str) + "-" + dim["MES"].astype(str).str.zfill(2)
    dim["TRIMESTRE"] = ((dim["MES"] - 1) // 3) + 1
    dim["SEMESTRE"] = dim["MES"].apply(lambda x: 1 if x <= 6 else 2)

    # COMPETENCIA (YYYYMM)
    dim["COMPETENCIA"] = dim["PERIODO"].astype(str).str.replace("-", "")

    # 🔴 AGORA sim converter PERIODO para string
    dim["PERIODO"] = dim["PERIODO"].astype(str)

    return dim.sort_values("COMPETENCIA").reset_index(drop=True)