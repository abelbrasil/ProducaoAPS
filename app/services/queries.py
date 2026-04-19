def get_base_query():
    return """
    SELECT 
        f."COMPETENCIA",
        f."CO_MUNICIPIO_IBGE",
        m."NO_MUNICIPIO",
        p."EXAME",
        f."ST_SOLICITADO",
        f."ST_AVALIADO",
        f."QT_EXM",
        f."QT_PRC"
    FROM apsdata."fato_prod_aps" f
    LEFT JOIN apsdata."dim_municipio" m
        ON f."CO_MUNICIPIO_IBGE"::text = m."CO_MUNICIPIO_IBGE"
    LEFT JOIN apsdata."dim_procedimentos" p
        ON f."CO_PROCEDIMENTO" = p."CO_EXAME"
    """