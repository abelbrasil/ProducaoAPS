import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# carregar .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

print("Testando conexão com o banco...\n")

try:
    # criar engine
    engine = create_engine(DATABASE_URL)

    # abrir conexão
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        value = result.scalar()

        print("✅ Conexão realizada com sucesso!")
        print(f"Resultado do teste: {value}")

except Exception as e:
    print("❌ Erro ao conectar no banco:")
    print(e)