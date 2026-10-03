from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from App.db import get_db
from App.models import *
from App.schemas import *
import App.crud as crud
import uvicorn


app = FastAPI()


@app.get('/')
def test():
    return {'message': 'hello world'}

#All Items in db
@app.get('/items/', response_model=list[ItemResponse])
def all_items(db:Session = Depends(get_db)):
    return crud.all_items_in_db(db)

#Aggiungi Item al database ufficiale
@app.post('/items/', response_model=ItemResponse)
def create_item(new_item:ItemCreate, db:Session = Depends(get_db)):
    return crud.add_item_to_database(db, new_item=new_item)
    
#Rimuovi item dal database ufficiale
@app.delete('/items/{item_code}')
def remove_item(item_code=str, db:Session = Depends(get_db)):
    return crud.remove_item_from_database(db, code = item_code)
    
#Visualizza un item in base al codice
@app.get('/items/{item_code}', response_model=ItemResponse)
def single_item(item_code:str, db:Session = Depends(get_db)):
    return crud.get_item_by_code(db, item_code=item_code)
    
#Tutto il contenuto del Magazzino
@app.get('/magazzino/', response_model=list[MagazzinoResponse])
def all_magazzino(db:Session = Depends(get_db)):
    return crud.all_items_in_magazzino(db)

#Aggiunge item al al Magazzino se il codice prodotto è presente nel database ufficiale!
@app.post('/magazzino/', response_model=MagazzinoResponse)
def add_magazzino(new_item: MagazzinoCreate, db:Session = Depends(get_db)):

   return crud.add_item_in_magazzino(db, new_item=new_item)
   
#Visualizza oggetto tramite codice presente in Magazzino
@app.get('/magazzino/{item_code}', response_model=MagazzinoResponse)
def single_item_magazzino(item_code:str, db:Session = Depends(get_db)):

    return crud.item_in_magazzino_by_code(db, code=item_code)

#Aggiungi quantità al magazzino in base al codice articolo
@app.put('/magazzino/{item_code}/add', response_model=MagazzinoResponse)
def update_item_magazzino(item:MagazzinoUpdate, item_code:str, db:Session = Depends(get_db)):
    return crud.add_quantity(db, item_update=item, item_code = item_code)

#Togli quantità al Magazzino in base al codice prodotto
@app.put('/magazzino/{item_code}/sottr', response_model=MagazzinoResponse)
def update_item_magazzino(item:MagazzinoUpdate, item_code:str, db:Session = Depends(get_db)):

   return crud.togli_quantità(db, item_update=item, item_code = item_code)
    
#Elimina item in Magazzino in base al codice    
@app.delete('/magazzino/{item_code}')
def delete_item_magazzino(item_code:str, db:Session = Depends(get_db)):

    return crud.delete_item_in_magazzino(db, code = item_code)



if __name__ == '__main__':
    
    uvicorn.run(app, host='0.0.0.0', port=5000)