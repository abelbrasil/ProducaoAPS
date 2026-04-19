import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# garantir que a pasta existe
os.makedirs("./db", exist_ok=True)

DATABASE_URL = "sqlite:///./db/aps.db"

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)