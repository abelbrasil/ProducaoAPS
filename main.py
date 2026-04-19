from src.pipeline.pipeline import executar_pipeline

fato, dim_proc, dim_cal, dim_mun = executar_pipeline()

print("\nFATO:")
print(fato.head())

print("\nDIM_PROCEDIMENTOS:")
print(dim_proc.head())

print("\nDIM_CALENDARIO:")
print(dim_cal.head())

print("\nDIM_MUNICIPIO:")
print(dim_mun.head())