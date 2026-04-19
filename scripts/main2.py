# %%
import pandas as pd

caminho_exames = "./data/exames_fortaleza.xlsx"

df_exames = pd.read_excel(caminho_exames)

#print(df_exames.head())

caminho_procedimentos = "./data/procedimentos.xlsx"

df_procedimentos = pd.read_excel(caminho_procedimentos)

#print(df_procedimentos.head())

# Verificar a estrutura dos DataFrames

#df_exames.info()
#df_procedimentos.info()

# Verificar a quantidade de caracteres em cada código

df_exames["QTD_CARAC"] = df_exames["CO_EXAME"].str.len()
df_procedimentos["QTD_CARAC"] = df_procedimentos["CO_PROCEDIMENTO"].str.len()

#print(df_exames["QTD_CARAC"].value_counts())
#print(df_procedimentos["QTD_CARAC"].value_counts())

# Identificar os códigos com 9 caracteres e adicionar um zero à esquerda

df_exames.loc[df_exames["QTD_CARAC"] == 9, "CO_EXAME"] = "0" + df_exames["CO_EXAME"]

df_procedimentos.loc[df_procedimentos["QTD_CARAC"] == 9, "CO_PROCEDIMENTO"] = "0" + df_procedimentos["CO_PROCEDIMENTO"]

# Verificar novamente a quantidade de caracteres após a correção

#df_exames["QTD_CARAC"] = df_exames["CO_EXAME"].str.len()
#df_procedimentos["QTD_CARAC"] = df_procedimentos["CO_PROCEDIMENTO"].str.len()

#print(df_exames["QTD_CARAC"].value_counts())
#print(df_procedimentos["QTD_CARAC"].value_counts())

# Separar os dataframes em 10 digitos e 7 digitos

df_exames_10_digitos = df_exames[df_exames["QTD_CARAC"] == 10]
df_procedimentos_10_digitos = df_procedimentos[df_procedimentos["QTD_CARAC"] == 10]

# Criar novos dataframes apenas com as colunas de código e nome do exame/procedimento

df_exames_10 = df_exames_10_digitos[["CO_EXAME", "EXAME"]].copy()
df_procedimentos_10 = df_procedimentos_10_digitos[["CO_PROCEDIMENTO", "PROCEDIMENTO"]].copy()
df_procedimentos_10.columns = ["CO_EXAME", "EXAME"]

df_unificado = pd.concat([df_exames_10, df_procedimentos_10], ignore_index=True)

df_unificado["FL_DUPLICADO"] = df_unificado.duplicated(subset=["CO_EXAME", "EXAME"],keep="first")

#print(df_unificado["FL_DUPLICADO"].value_counts())

df_unificado = df_unificado[df_unificado["FL_DUPLICADO"] == False].sort_values(by="CO_EXAME")

df_unificado["FL_DUPLI_CO"] = df_unificado.duplicated(subset=["CO_EXAME"],keep=False)
df_unificado["FL_DUPLI_NM"] = df_unificado.duplicated(subset=["EXAME"],keep=False)

print(df_unificado["FL_DUPLI_CO"].value_counts())
print(df_unificado["FL_DUPLI_NM"].value_counts())

# --------------------------------------------------------------

df_exames_7_digitos = df_exames[df_exames["QTD_CARAC"] == 7]
df_procedimentos_7_digitos = df_procedimentos[df_procedimentos["QTD_CARAC"] == 7]

# Padronizar colunas
df_exames_7 = df_exames_7_digitos[["CO_EXAME", "EXAME"]].copy()

df_procedimentos_7 = df_procedimentos_7_digitos[["CO_PROCEDIMENTO", "PROCEDIMENTO"]].copy()
df_procedimentos_7.columns = ["CO_EXAME", "EXAME"]

# Unificar
df_unificado_7 = pd.concat([df_exames_7, df_procedimentos_7],ignore_index=True)

# Flag duplicidade exata (código + nome)
df_unificado_7["FL_DUPLICADO"] = df_unificado_7.duplicated(subset=["CO_EXAME", "EXAME"], keep="first")

# Remover duplicados exatos
df_unificado_7 = df_unificado_7[df_unificado_7["FL_DUPLICADO"] == False].sort_values(by="CO_EXAME")

# Flags adicionais
df_unificado_7["FL_DUPLI_CO"] = df_unificado_7.duplicated(subset=["CO_EXAME"],keep=False)
df_unificado_7["FL_DUPLI_NM"] = df_unificado_7.duplicated(subset=["EXAME"],keep=False)

# Validação
print(df_unificado_7["FL_DUPLI_CO"].value_counts())
print(df_unificado_7["FL_DUPLI_NM"].value_counts())

# --------------------------------------------------------------

tb_dim_procedimentos = pd.concat([df_unificado, df_unificado_7], ignore_index=True)