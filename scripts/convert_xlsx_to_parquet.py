import os
import pandas as pd

# ==============================
# CONFIGURAÇÕES
# ==============================

DATA_DIR = "./data"
PARQUET_DIR = os.path.join(DATA_DIR, "parquet")

# ==============================
# GARANTIR PASTA DE DESTINO
# ==============================

os.makedirs(PARQUET_DIR, exist_ok=True)

# ==============================
# IDENTIFICAR ARQUIVOS XLSX
# ==============================

arquivos = [f for f in os.listdir(DATA_DIR) if f.endswith(".xlsx")]

if not arquivos:
    print("Nenhum arquivo .xlsx encontrado na pasta /data")
    exit()

# ==============================
# PROCESSAMENTO
# ==============================

print(f"Encontrados {len(arquivos)} arquivos .xlsx\n")

for arquivo in arquivos:

    caminho_xlsx = os.path.join(DATA_DIR, arquivo)
    nome_base = os.path.splitext(arquivo)[0]
    caminho_parquet = os.path.join(PARQUET_DIR, f"{nome_base}.parquet")

    print(f"Processando: {arquivo}")

    try:
        # leitura
        df = pd.read_excel(caminho_xlsx)

        # exportação
        df.to_parquet(caminho_parquet, index=False)

        print(f"✔ Convertido para: {caminho_parquet}\n")

    except Exception as e:
        print(f"✖ Erro ao processar {arquivo}: {e}\n")

print("Processo finalizado.")