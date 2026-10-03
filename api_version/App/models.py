from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import declarative_base
from App.db import engine

Base = declarative_base()

#Sqlalchemy models
class BaseModello(Base):
    __abstract__ = True
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True)

class Magazzino(BaseModello):
    __tablename__ = 'magazzino'

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer)


class Item(BaseModello):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False, unique=True)

Base.metadata.create_all(engine)

