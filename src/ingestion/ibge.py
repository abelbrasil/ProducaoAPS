import requests
import pandas as pd

def get_ibge_municipios():
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Erro ao acessar API IBGE: {response.status_code}")

    dados = response.json()

    df_flat = pd.json_normalize(dados)

    df_ibge = pd.DataFrame({
        "CO_MUNICIPIO_IBGE": df_flat["id"].astype(str),
        "NO_MUNICIPIO": df_flat["nome"].str.strip(),
        "UF": df_flat["microrregiao.mesorregiao.UF.sigla"],
        "NO_UF": df_flat["microrregiao.mesorregiao.UF.nome"],
        "REGIAO": df_flat["microrregiao.mesorregiao.UF.regiao.nome"]
    })

    return df_ibge