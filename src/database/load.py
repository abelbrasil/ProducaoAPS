from src.database.connection import engine

def carregar_dataframe(df, tabela_nome, schema="apsdata"):

    print(f"➡️ Enviando {schema}.{tabela_nome} ({len(df)} registros)...")

    # garantir tipos compatíveis
    for col in df.columns:
        if "period" in str(df[col].dtype):
            df[col] = df[col].astype(str)
            
    df.to_sql(
        tabela_nome,
        con=engine,
        schema=schema,
        if_exists="replace",
        index=False,
        method="multi",
        chunksize=2000
    )

    print(f"✔ {schema}.{tabela_nome} carregada com sucesso!\n")