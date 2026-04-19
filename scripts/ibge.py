
import requests
import pandas as pd

# ==============================
# 1. CONSUMO DA API
# ==============================

url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"

print("Consultando API do IBGE...")

response = requests.get(url)

if response.status_code != 200:
    raise Exception(f"Erro ao acessar API IBGE: {response.status_code}")

dados = response.json()

print(f"Total de municípios retornados: {len(dados)}")

# ==============================
# 2. NORMALIZAÇÃO DO JSON
# ==============================

df_flat = pd.json_normalize(dados)

# visualizar colunas (debug inicial)
print("\nColunas disponíveis:")
print(df_flat.columns.tolist())

# ==============================
# 3. CRIAÇÃO DO DATAFRAME FINAL
# ==============================

df_ibge_municipios = pd.DataFrame({
    "CO_MUNICIPIO_IBGE": df_flat["id"].astype(str),
    "NO_MUNICIPIO": df_flat["nome"].str.strip(),
    "UF": df_flat["microrregiao.mesorregiao.UF.sigla"],
    "NO_UF": df_flat["microrregiao.mesorregiao.UF.nome"],
    "REGIAO": df_flat["microrregiao.mesorregiao.UF.regiao.nome"]
})

# ==============================
# 4. TRATAMENTO DE NULOS
# ==============================

df_ibge_municipios["UF"] = df_ibge_municipios["UF"].fillna("NA")
df_ibge_municipios["NO_UF"] = df_ibge_municipios["NO_UF"].fillna("NA")
df_ibge_municipios["REGIAO"] = df_ibge_municipios["REGIAO"].fillna("NA")

# ==============================
# 5. VALIDAÇÃO
# ==============================

print("\nPreview IBGE:")
print(df_ibge_municipios.head())

print("\nShape:")
print(df_ibge_municipios.shape)

print("\nValores nulos por coluna:")
print(df_ibge_municipios.isna().sum())
