from src.pipeline.pipeline import executar_pipeline
from src.database.load import criar_banco, carregar_dataframe

# executa pipeline
fato, dim_proc, dim_cal, dim_mun = executar_pipeline()

# cria banco
criar_banco()

# carga
carregar_dataframe(fato, "fato_prod_aps")
carregar_dataframe(dim_proc, "dim_procedimentos")
carregar_dataframe(dim_cal, "dim_calendario")
carregar_dataframe(dim_mun, "dim_municipio")

print("Banco SQLite criado e carregado com sucesso.")