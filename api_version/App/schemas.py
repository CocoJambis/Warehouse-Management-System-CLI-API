from pydantic import BaseModel, ConfigDict

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

    model_config = ConfigDict(from_attributes = True)


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

    model_config = ConfigDict(from_attributes = True)

class MagazzinoUpdate(BaseModel):
    quantity:int