import pytest
from fastapi import HTTPException
from App.schemas import *
from App.models import *
from App.crud import *



def test_add_item_in_database(db_session):
    item_in = ItemCreate(code = "POP123", name = "Coca Sleek")
    item = add_item_to_database(db_session, item_in)

    assert item is not None
    assert item.code == "POP123"
    assert item.name == "COCA SLEEK"

def test_add_item_in_database_already_existing(db_session):
    item_in = ItemCreate(code = "POP123", name= "coca sleek")
    item = add_item_to_database(db_session, item_in)

    with pytest.raises(HTTPException) as exc_info:
        add_item_to_database(db_session, item_in)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Item già nel database"

def test_remove_item_from_database(db_session):
    item_in = ItemCreate(code= "POP123", name = "coca sleek")
    item = add_item_to_database(db_session, item_in)

    message = remove_item_from_database(db_session, item_in.code)

    with pytest.raises(HTTPException) as exc_info:
        item_get = get_item_by_code(db_session, item_in.code)

    assert message == f"{item_in.code} deleted!"
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Item non esistente nel database"
   
def test_remove_item_from_database_not_existing(db_session):

    with pytest.raises(HTTPException) as exc_info:
        remove_item_from_database(db_session, "POP123")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Item non esistente nel database"

def test_get_item_by_code(db_session):
    item_in = ItemCreate(code = "POP123", name = "coca sleek")
    item = add_item_to_database(db_session, item_in)

    assert get_item_by_code(db_session, "POP123") is not None


def test_add_item_to_magazzino(db_session):

    item_db = ItemCreate(code = "POP123", name = "coca sleek")
    item = add_item_to_database(db_session, item_db)

    item_magazzino = MagazzinoCreate(code = "POP123", quantity = 10)
    item_magazzino_add = add_item_in_magazzino(db_session, item_magazzino)

    assert item_magazzino_add.code == "POP123"
    assert item_magazzino_add.quantity == 10

def test_add_item_to_magazzino_no_item_in_database(db_session):

    item_magazzino = MagazzinoCreate(code = "POP123", quantity=10)

    with pytest.raises(HTTPException) as exc_info:
        item = add_item_in_magazzino(db_session, item_magazzino)


    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Item non presente nel database ufficiale"

def test_add_item_to_magazzino_already_in(db_session):
    item_db = ItemCreate(code = "POP123", name = "coca sleek")
    item = add_item_to_database(db_session, item_db)

    item_magazzino = MagazzinoCreate(code = "POP123", quantity = 10)
    item_magazzino_add = add_item_in_magazzino(db_session, item_magazzino)

    with pytest.raises(HTTPException) as exc_info:
        add_item_in_magazzino(db_session, item_magazzino)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Item già esistente nel magazzino"


def test_view_item_in_magazzino_by_code(db_session):
    item_db = ItemCreate(code = "POP123", name = "coca sleek")
    item = add_item_to_database(db_session, item_db)

    item_magazzino = MagazzinoCreate(code = "POP123", quantity = 10)
    item_magazzino_add = add_item_in_magazzino(db_session, item_magazzino)

    assert item_in_magazzino_by_code(db_session, item.code) is not None
    assert item.code == "POP123"
    assert item.name == "COCA SLEEK"

def test_add_quantity(db_session):
    item_db = ItemCreate(code = "POP123", name = "coca sleek")
    item = add_item_to_database(db_session, item_db)

    item_magazzino = MagazzinoCreate(code = "POP123", quantity = 10)
    item_magazzino_add = add_item_in_magazzino(db_session, item_magazzino)

    magazzino_update = MagazzinoUpdate(quantity = 10)

    add_quantity(db_session, item_update=magazzino_update, item_code = item_magazzino_add.code)

    assert item_magazzino_add.quantity == 20

def test_add_quantity_not_exsisting(db_session):
    item_db = ItemCreate(code = "POP123", name = "coca sleek")
    item = add_item_to_database(db_session, item_db)

    item_magazzino = MagazzinoCreate(code = "POP123", quantity = 10)
    item_magazzino_add = add_item_in_magazzino(db_session, item_magazzino)

    magazzino_update = MagazzinoUpdate(quantity = 10)

    with pytest.raises(HTTPException) as exc_info:
        add_quantity(db_session, item_update=magazzino_update, item_code = "POP456")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "POP456 non presente in magazzino"


def test_togli_quantità(db_session):
    item_db = ItemCreate(code = "POP123", name = "coca sleek")
    item = add_item_to_database(db_session, item_db)

    item_magazzino = MagazzinoCreate(code = "POP123", quantity = 10)
    item_magazzino_add = add_item_in_magazzino(db_session, item_magazzino)

    magazzino_update = MagazzinoUpdate(quantity = 10)

    togli_quantità(db_session, item_update=magazzino_update, item_code = item_magazzino_add.code)

    assert item_magazzino_add.quantity == 0


def test_remove_item_in_magazzino(db_session):
    item_db = ItemCreate(code = "POP123", name = "coca sleek")
    item = add_item_to_database(db_session, item_db)

    item_magazzino = MagazzinoCreate(code = "POP123", quantity = 10)
    item_magazzino_add = add_item_in_magazzino(db_session, item_magazzino)

    message = delete_item_in_magazzino(db_session, item_magazzino_add.code)

    with pytest.raises(HTTPException) as exc_info:
        item_find = item_in_magazzino_by_code(db_session, item_magazzino_add.code)

    assert message == f"{item_magazzino_add.code} eliminato da Magazzino!"
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Item non presente in magazzino"


def test_togli_quantità_fail(db_session):
    item_db = ItemCreate(code = "POP123", name = "coca sleek")
    item = add_item_to_database(db_session, item_db)

    item_magazzino = MagazzinoCreate(code = "POP123", quantity = 10)
    item_magazzino_add = add_item_in_magazzino(db_session, item_magazzino)

    magazzino_update = MagazzinoUpdate(quantity = 20)

    with pytest.raises(HTTPException) as exc_info:
        togli_quantità(db_session, item_update=magazzino_update, item_code = item_magazzino_add.code)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f"Impossibile sottrarre la quantità inserita, quantità disponibile : {item_magazzino_add.quantity}"