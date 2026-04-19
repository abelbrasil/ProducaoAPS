from src.pipeline.pipeline import executar_pipeline
from src.database.load import carregar_dataframe

print("\n🚀 Iniciando pipeline...\n")

# executar pipeline
fato, dim_proc, dim_cal, dim_mun = executar_pipeline()

print("✔ Pipeline executado")
print(f"FATO: {fato.shape}")
print(f"DIM_PROCEDIMENTOS: {dim_proc.shape}")
print(f"DIM_CALENDARIO: {dim_cal.shape}")
print(f"DIM_MUNICIPIO: {dim_mun.shape}\n")

# carga
print("📦 Enviando dados para o Supabase...\n")

carregar_dataframe(fato, "fato_prod_aps", schema="apsdata")
print("✔ fato_prod_aps carregada")

carregar_dataframe(dim_proc, "dim_procedimentos", schema="apsdata")
print("✔ dim_procedimentos carregada")

carregar_dataframe(dim_cal, "dim_calendario", schema="apsdata")
print("✔ dim_calendario carregada")

carregar_dataframe(dim_mun, "dim_municipio", schema="apsdata")
print("✔ dim_municipio carregada")

print("\n🎯 Carga no Postgres (Supabase) finalizada com sucesso!\n")