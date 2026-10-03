from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from api_version.App.db import get_db
from api_version.App.models import Magazzino, Item, ItemCreate, MagazzinoCreate, ItemResponse, MagazzinoResponse, MagazzinoUpdate
import uvicorn


app = FastAPI()


@app.get('/')
def test():
    return {'message': 'hello world'}

#All Items in db
@app.get('/items/', response_model=list[ItemResponse])
def all_items(db:Session = Depends(get_db)):
    return db.query(Item).all()

#Aggiungi Item al database ufficiale
@app.post('/items/', response_model=ItemResponse)
def create_item(new_item:ItemCreate, db:Session = Depends(get_db)):
    if db.query(Item).filter(Item.code == new_item.code.upper()).one_or_none():
        raise HTTPException(status_code=404, detail='Item già nel database')
    else:
        new_item = Item(code = new_item.code.upper(), name = new_item.name.upper())
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item
    
#Rimuovi item dal database ufficiale
@app.delete('/items/{item_code}')
def remove_item(item_code=str, db:Session = Depends(get_db)):
    item = db.query(Item).filter(Item.code == item_code.upper()).one_or_none()

    if item:
        db.delete(item)
        db.commit()
        return {'message': 'Item Deleted'}
    else:
        raise HTTPException(status_code= 404, detail='Item non esistente nel database')
    
#Visualizza un item in base al codice
@app.get('/items/{item_code}', response_model=ItemResponse)
def single_item(item_code:str, db:Session = Depends(get_db)):
    item = db.query(Item).filter_by(code=item_code.upper()).one_or_none()

    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail='Item non esistente nel database')
    
#Tutto il contenuto del Magazzino
@app.get('/magazzino/', response_model=list[MagazzinoResponse])
def all_magazzino(db:Session = Depends(get_db)):
    return db.query(Magazzino).all()

#Aggiunge item al al Magazzino se il codice prodotto è presente nel database ufficiale!
@app.post('/magazzino/', response_model=MagazzinoResponse)
def add_magazzino(new_item: MagazzinoCreate, db:Session = Depends(get_db)):

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
@app.get('/magazzino/{item_code}', response_model=MagazzinoResponse)
def single_item_magazzino(item_code:str, db:Session = Depends(get_db)):

    item = db.query(Magazzino).filter(Magazzino.code == item_code.upper()).one_or_none()

    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail='Item non presente in magazzino')

#Aggiungi quantità al magazzino in base al codice articolo
@app.put('/magazzino/{item_code}/add', response_model=MagazzinoResponse)
def update_item_magazzino(item:MagazzinoUpdate, item_code:str, db:Session = Depends(get_db)):

    item_magazzino = db.query(Magazzino).filter(Magazzino.code == item_code.upper()).one_or_none()

    if not item_magazzino:
        raise HTTPException(status_code=404, detail=f'{item_code} non presente in magazzino')
    
    item_magazzino.quantity += item.quantity

    db.commit()
    db.refresh(item_magazzino)
    return item_magazzino

#Togli quantità al Magazzino in base al codice prodotto
@app.put('/magazzino/{item_code}/sottr', response_model=MagazzinoResponse)
def update_item_magazzino(item:MagazzinoUpdate, item_code:str, db:Session = Depends(get_db)):

    item_magazzino = db.query(Magazzino).filter(Magazzino.code == item_code.upper()).one_or_none()

    if not item_magazzino:
        raise HTTPException(status_code=404, detail=f'{item_code}non presente in magazzino')
    
    if item.quantity <= item_magazzino.quantity:
        item_magazzino.quantity -= item.quantity
        db.commit()
        db.refresh(item_magazzino)
        return item_magazzino
    else:
        raise HTTPException(status_code=404, detail=f'Impossibile sottrarre la quantità inserita, quantità disponibile : {item_magazzino.quantity}')
    
#Elimina item in Magazzino in base al codice    
@app.delete('/magazzino/{item_code}')
def delete_item_magazzino(item_code:str, db:Session = Depends(get_db)):

    item = db.query(Magazzino).filter(Magazzino.code == item_code.upper()).one_or_none()

    if item:
        db.delete(item)
        db.commit()
        return f'{item.code} eliminato da Magazzino!'
    else:
        raise HTTPException(status_code=404, detail=f'{item_code} non presente in magazzino')
    


if __name__ == '__main__':
    
    uvicorn.run(app, host='0.0.0.0', port=5000)