from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# ======================
# FATO
# ======================
class FatoAPS(Base):
    __tablename__ = "fato_prod_aps"

    COMPETENCIA = Column(String, primary_key=True)
    CO_MUNICIPIO_IBGE = Column(String, primary_key=True)
    CO_PROCEDIMENTO = Column(String, primary_key=True)

    ST_SOLICITADO = Column(Float)
    ST_AVALIADO = Column(Float)
    QT_EXM = Column(Float)
    QT_PRC = Column(Float)

# ======================
# DIM_PROCEDIMENTOS
# ======================
class DimProcedimentos(Base):
    __tablename__ = "dim_procedimentos"

    CO_EXAME = Column(String, primary_key=True)
    EXAME = Column(String)

    FL_DUPLICADO = Column(Integer)
    FL_DUPLI_CO = Column(Integer)
    FL_DUPLI_NM = Column(Integer)
    FL_INCONSISTENTE = Column(Integer)
    FL_SEM_DESCRICAO = Column(Integer)
    TP_CODIGO = Column(Integer)

# ======================
# DIM_CALENDARIO
# ======================
class DimCalendario(Base):
    __tablename__ = "dim_calendario"

    COMPETENCIA = Column(String, primary_key=True)

    ANO = Column(Integer)
    MES = Column(Integer)
    NOME_MES = Column(String)
    ANO_MES = Column(String)
    TRIMESTRE = Column(Integer)
    SEMESTRE = Column(Integer)

# ======================
# DIM_MUNICIPIO
# ======================
class DimMunicipio(Base):
    __tablename__ = "dim_municipio"

    CO_MUNICIPIO_IBGE = Column(String, primary_key=True)

    NO_MUNICIPIO = Column(String)
    UF = Column(String)
    NO_UF = Column(String)
    REGIAO = Column(String)
    FL_NAO_ENCONTRADO = Column(Integer)