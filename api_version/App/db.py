from sqlalchemy import  create_engine
from sqlalchemy.orm import  sessionmaker
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:1312@localhost:5432/Magazzino')

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Connessione al Database
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()