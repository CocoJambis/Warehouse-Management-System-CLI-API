from fastapi import HTTPException
from sqlalchemy.orm import Session
from .models import *
from .schemas import *

#All Items in db
def all_items_in_db(db:Session) -> list[object]:
    return db.query(Item).all() 

#Aggiungi Item al database ufficiale
def add_item_to_database(db:Session, new_item:ItemCreate) -> None:
    if db.query(Item).filter(Item.code == new_item.code.upper()).one_or_none():
            raise HTTPException(status_code=404, detail='Item già nel database')
    else:
        new_item = Item(code = new_item.code.upper(), name = new_item.name.upper())
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item

#Rimuovi item dal database ufficiale
def remove_item_from_database(db:Session, code:str) -> None:
    item = db.query(Item).filter(Item.code == code.upper()).one_or_none()

    if item:
        db.delete(item)
        db.commit()
        return f"{item.code} deleted!"
    else:
        raise HTTPException(status_code= 404, detail='Item non esistente nel database')

#Visualizza un item in base al codice
def get_item_by_code(db:Session, item_code:str) -> object:
    item = db.query(Item).filter_by(code=item_code.upper()).one_or_none()

    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail='Item non esistente nel database')

#Tutto il contenuto del Magazzino
def all_items_in_magazzino(db:Session) -> list[object]:
    return db.query(Magazzino).all()

#Aggiunge item al al Magazzino se il codice prodotto è presente nel database ufficiale!
def add_item_in_magazzino(db:Session, new_item:MagazzinoCreate) -> None:
    item_db = db.query(Item).filter(Item.code == new_item.code.upper()).first()

    if db.query(Magazzino).filter(Magazzino.code == new_item.code.upper()).first():
        raise HTTPException(status_code=404, detail='Item già esistente nel magazzino')
    elif item_db:
        item = Magazzino(code = item_db.code, name = item_db.name, quantity = new_item.quantity)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    else:
        raise HTTPException(status_code=404, detail='Item non presente nel database ufficiale')

#Visualizza oggetto tramite codice presente in Magazzino
def item_in_magazzino_by_code(db:Session, code:str) -> object:
    item = db.query(Magazzino).filter(Magazzino.code == code.upper()).one_or_none()

    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail='Item non presente in magazzino')

#Aggiungi quantità al magazzino in base al codice articolo
def add_quantity(db:Session, item_update:MagazzinoUpdate, item_code:str) -> None:
    
    item_magazzino = db.query(Magazzino).filter(Magazzino.code == item_code.upper()).one_or_none()

    if not item_magazzino:
        raise HTTPException(status_code=404, detail=f'{item_code} non presente in magazzino')
    
    item_magazzino.quantity += item_update.quantity

    db.commit()
    db.refresh(item_magazzino)
    return item_magazzino


#Togli quantità al Magazzino in base al codice prodotto
def togli_quantità(db:Session, item_update:MagazzinoUpdate, item_code:str) -> None:
    item_magazzino = db.query(Magazzino).filter(Magazzino.code == item_code.upper()).one_or_none()

    if not item_magazzino:
        raise HTTPException(status_code=404, detail=f'{item_code}non presente in magazzino')
    
    if item_update.quantity <= item_magazzino.quantity:
        item_magazzino.quantity -= item_update.quantity
        db.commit()
        db.refresh(item_magazzino)
        return item_magazzino
    else:
        raise HTTPException(status_code=404, detail=f'Impossibile sottrarre la quantità inserita, quantità disponibile : {item_magazzino.quantity}')


#Elimina item in Magazzino in base al codice    
def delete_item_in_magazzino(db:Session, code:str) -> None:
    item = db.query(Magazzino).filter(Magazzino.code == code.upper()).one_or_none()

    if item:
        db.delete(item)
        db.commit()
        return f'{item.code} eliminato da Magazzino!'
    else:
        raise HTTPException(status_code=404, detail=f'{code} non presente in magazzino')