
import pandas as pd

# ==============================
# 1. LEITURA
# ==============================

df_exames = pd.read_excel("./data/exames_fortaleza.xlsx")
df_procedimentos = pd.read_excel("./data/procedimentos.xlsx")

# ==============================
# 2. PADRONIZAÇÃO
# ==============================

def padronizar_codigo(df, coluna):
    return df[coluna].fillna("").astype(str).str.zfill(10)

df_exames["CO_EXAME"] = padronizar_codigo(df_exames, "CO_EXAME")
df_procedimentos["CO_PROCEDIMENTO"] = padronizar_codigo(df_procedimentos, "CO_PROCEDIMENTO")

# ==============================
# 3. BASE UNIFICADA (FATO)
# ==============================

df_exames_fato = df_exames.rename(columns={"CO_EXAME": "CO_PROCEDIMENTO"})

df_procedimentos_fato = df_procedimentos.copy()

df_base = pd.concat([df_exames_fato, df_procedimentos_fato], ignore_index=True)

# ==============================
# 4. AGREGAÇÃO (FATO)
# ==============================

fato_prod_aps = (
    df_base
    .groupby(
        ["COMPETENCIA", "CO_MUNICIPIO_IBGE", "CO_PROCEDIMENTO"],
        as_index=False)
    .agg({
        "ST_SOLICITADO": "sum",
        "ST_AVALIADO": "sum",
        "QT_EXM": "sum",
        "QT_PRC": "sum"
    })
)

# ==============================
# 5. DIMENSÃO (BASE)
# ==============================

df_dim_exames = df_exames[["CO_EXAME", "EXAME"]].copy()

df_dim_proc = df_procedimentos[["CO_PROCEDIMENTO", "PROCEDIMENTO"]].copy()
df_dim_proc.columns = ["CO_EXAME", "EXAME"]

dim_procedimentos = pd.concat([df_dim_exames, df_dim_proc], ignore_index=True)

# ==============================
# 6. LIMPEZA DE DUPLICADOS EXATOS
# ==============================

dim_procedimentos["FL_DUPLICADO"] = dim_procedimentos.duplicated(["CO_EXAME", "EXAME"], keep="first")

dim_procedimentos = dim_procedimentos[~dim_procedimentos["FL_DUPLICADO"]]

# ==============================
# 7. FLAGS DE QUALIDADE
# ==============================

# duplicidade por código
dim_procedimentos["FL_DUPLI_CO"] = dim_procedimentos.duplicated(["CO_EXAME"], keep=False)

# duplicidade por nome
dim_procedimentos["FL_DUPLI_NM"] = dim_procedimentos.duplicated(["EXAME"], keep=False)

# inconsistência (mesmo código com nomes diferentes)
map_inconsistencia = (
    dim_procedimentos
    .groupby("CO_EXAME")["EXAME"]
    .nunique()
    .gt(1)
)

dim_procedimentos["FL_INCONSISTENTE"] = dim_procedimentos["CO_EXAME"].map(map_inconsistencia)

# tipo do código (7 ou 10 dígitos)
dim_procedimentos["TP_CODIGO"] = dim_procedimentos["CO_EXAME"].str.len()

# ordenar dim_procedimentos por código
dim_procedimentos = dim_procedimentos.sort_values("CO_EXAME").reset_index(drop=True) 

# ==============================
# 8. VALIDAÇÃO
# ==============================

#print("FATO:")
#print(fato_prod_aps.head())

#print("\nDIMENSÃO:")
#print(dim_procedimentos.head())

#print("\nResumo Flags:")
#print(dim_procedimentos[["FL_DUPLI_CO", "FL_DUPLI_NM", "FL_INCONSISTENTE"]].sum())

# ==============================
# 9. EXPORTAÇÃO
# ==============================

#fato_prod_aps.to_excel("./output/fato_prod_aps.xlsx", index=False)
#dim_procedimentos.to_excel("./output/dim_procedimentos.xlsx", index=False)

# ==============================
# 10. TRATAMENTO DE MISSING NA DIMENSÃO
# ==============================

# Flag: nome vazio ou missing
dim_procedimentos["FL_NOME_VAZIO"] = (
    dim_procedimentos["EXAME"].isna() | (dim_procedimentos["EXAME"].str.strip() == "")
)

# Identificar códigos que possuem pelo menos um nome válido
codigos_com_nome_valido = (
    dim_procedimentos
    .groupby("CO_EXAME")["FL_NOME_VAZIO"]
    .apply(lambda x: (~x).any())  # existe pelo menos um nome válido
)

# Mapear essa informação na base
dim_procedimentos["FL_TEM_NOME_VALIDO"] = dim_procedimentos["CO_EXAME"].map(codigos_com_nome_valido)

# ==============================
# REGRA 1:
# Remover missing quando existe nome válido para o mesmo código
# ==============================

dim_procedimentos = dim_procedimentos[
    ~(
        (dim_procedimentos["FL_NOME_VAZIO"]) &
        (dim_procedimentos["FL_TEM_NOME_VALIDO"])
    )
]

# ==============================
# REGRA 2:
# Flag para códigos sem nenhuma descrição
# ==============================

dim_procedimentos["FL_SEM_DESCRICAO"] = (
    dim_procedimentos
    .groupby("CO_EXAME")["FL_NOME_VAZIO"]
    .transform(lambda x: x.all())  # todos são vazios
)

# ==============================
# LIMPEZA FINAL (opcional)
# ==============================

dim_procedimentos = dim_procedimentos.drop(columns=[
    "FL_NOME_VAZIO",
    "FL_TEM_NOME_VALIDO"
])

# Reordenar
dim_procedimentos = dim_procedimentos.sort_values("CO_EXAME").reset_index(drop=True)

# ==============================
# 11. RECÁLCULO DAS FLAGS (APÓS LIMPEZA)
# ==============================

# Recalcular duplicidade exata
dim_procedimentos["FL_DUPLICADO"] = dim_procedimentos.duplicated(
    ["CO_EXAME", "EXAME"], keep="first"
)

# Recalcular duplicidade por código
dim_procedimentos["FL_DUPLI_CO"] = dim_procedimentos.duplicated(
    ["CO_EXAME"], keep=False
)

# Recalcular duplicidade por nome
dim_procedimentos["FL_DUPLI_NM"] = dim_procedimentos.duplicated(
    ["EXAME"], keep=False
)

# Recalcular inconsistência (mesmo código com nomes diferentes)
map_inconsistencia = (
    dim_procedimentos
    .groupby("CO_EXAME")["EXAME"]
    .nunique()
    .gt(1)
)

dim_procedimentos["FL_INCONSISTENTE"] = dim_procedimentos["CO_EXAME"].map(map_inconsistencia)

# Reordenar novamente
dim_procedimentos = dim_procedimentos.sort_values("CO_EXAME").reset_index(drop=True)

# ==============================
# 12.1 DIM_CALENDARIO
# ==============================

# Garantir que COMPETENCIA está como string
fato_prod_aps["COMPETENCIA"] = fato_prod_aps["COMPETENCIA"].astype(str)

# Identificar período mínimo e máximo
periodo_min = fato_prod_aps["COMPETENCIA"].min()
periodo_max = fato_prod_aps["COMPETENCIA"].max()

# Criar sequência mensal
dim_calendario = pd.DataFrame({
    "COMPETENCIA": pd.period_range(
        start=periodo_min,
        end=periodo_max,
        freq="M"
    ).astype(str)
})

# Colunas auxiliares
dim_calendario["ANO"] = dim_calendario["COMPETENCIA"].str[:4].astype(int)
dim_calendario["MES"] = dim_calendario["COMPETENCIA"].str[4:6].astype(int)

# Nome dos meses
map_meses = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

dim_calendario["NOME_MES"] = dim_calendario["MES"].map(map_meses)

# Campos adicionais
dim_calendario["ANO_MES"] = dim_calendario["ANO"].astype(str) + "-" + dim_calendario["MES"].astype(str).str.zfill(2)
dim_calendario["TRIMESTRE"] = ((dim_calendario["MES"] - 1) // 3) + 1
dim_calendario["SEMESTRE"] = dim_calendario["MES"].apply(lambda x: 1 if x <= 6 else 2)

# Ordenar
dim_calendario = dim_calendario.sort_values("COMPETENCIA").reset_index(drop=True)

# ==============================
# 12.2 DIM_MUNICIPIO
# ==============================

# Extrair municípios únicos da fato
dim_municipio = fato_prod_aps[["CO_MUNICIPIO_IBGE"]].drop_duplicates().copy()

# Garantir tipo string
dim_municipio["CO_MUNICIPIO_IBGE"] = dim_municipio["CO_MUNICIPIO_IBGE"].astype(str)

# ------------------------------
# Carregar base do IBGE (ajustar caminho conforme download)
# ------------------------------
df_ibge = pd.read_excel("./data/ibge_municipios.xlsx")

# Ajustar nomes das colunas (depende do arquivo IBGE)
df_ibge = df_ibge.rename(columns={
    "Código Município Completo": "CO_MUNICIPIO_IBGE",
    "Nome_Município": "NO_MUNICIPIO"
})

# Garantir tipo string
df_ibge["CO_MUNICIPIO_IBGE"] = df_ibge["CO_MUNICIPIO_IBGE"].astype(str)

# Join
dim_municipio = dim_municipio.merge(
    df_ibge[["CO_MUNICIPIO_IBGE", "NO_MUNICIPIO"]],
    on="CO_MUNICIPIO_IBGE",
    how="left"
)

# ------------------------------
# Flag de município não encontrado
# ------------------------------
dim_municipio["FL_NAO_ENCONTRADO"] = dim_municipio["NO_MUNICIPIO"].isna()

# Ordenar
dim_municipio = dim_municipio.sort_values("CO_MUNICIPIO_IBGE").reset_index(drop=True)

# ==============================
# 12.3 VALIDAÇÃO
# ==============================

print("DIM_CALENDARIO:")
print(dim_calendario.head())

print("\nDIM_MUNICIPIO:")
print(dim_municipio.head())

print("\nMunicípios sem correspondência IBGE:")
print(dim_municipio["FL_NAO_ENCONTRADO"].sum())

# ==============================
# 12.4 EXPORTAÇÃO
# ==============================

#dim_calendario.to_excel("./output/dim_calendario.xlsx", index=False)
#dim_municipio.to_excel("./output/dim_municipio.xlsx", index=False)
