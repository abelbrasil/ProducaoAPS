def padronizar_codigo(df, coluna):
    return df[coluna].fillna("").astype(str).str.zfill(10)