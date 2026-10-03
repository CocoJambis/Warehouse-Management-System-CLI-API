from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel
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

#Pydantic models Item
class ItemBase(BaseModel):
    code:str
    name:str

class ItemCreate(ItemBase):
    pass

class ItemResponse(BaseModel):
    id:int
    code:str
    name:str

    class Config:
        from_attributes = True


#Pydantic models Magazzino
class MagazzinoBase(BaseModel):
    code:str
    quantity:int

class MagazzinoCreate(MagazzinoBase):
    pass

class MagazzinoResponse(BaseModel):
    id:int
    code:str
    name:str
    quantity:int

    class Config:
        from_attributes = True

class MagazzinoUpdate(BaseModel):
    quantity:int