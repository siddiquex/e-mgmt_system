from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.db import get_db
from app import models, schemas
from typing import List

LOW_STOCK_THRESHOLD = 10

router = APIRouter(
        prefix='/inventory',
        tags=['Inventory'],
        responses={404: {"description": "Not found"}}
    )

@router.post('/', response_model=schemas.Inventory)
def add_to_inventory(inventory_item: schemas.InventoryCreate, db: Session = Depends(get_db)):
    new_inventory_item = models.Inventory(**inventory_item.model_dump())
    db.add(new_inventory_item)
    db.commit()
    db.refresh(new_inventory_item)
    return new_inventory_item


@router.get("/low_stock", response_model=List[schemas.Inventory])
def get_item_low_in_stock(db: Session = Depends(get_db)):
    items_in_low_stock = db.query(models.Inventory).filter(models.Inventory.in_stock < LOW_STOCK_THRESHOLD).all()
    return items_in_low_stock


@router.get('/', response_model=List[schemas.Inventory])
def get_inventory(db: Session = Depends(get_db)):
    inventory = db.query(models.Inventory).all()
    return inventory


@router.get('/{inventory_id}', response_model=schemas.Inventory)
def get_inventory_item(inventory_id, db: Session = Depends(get_db)):
    inventory_item = db.query(models.Inventory).filter(models.Inventory.inventory_id == inventory_id).first()
    if inventory_item is None:
        raise HTTPException(status_code=404, detail='Inventory item not found')
    return inventory_item


@router.patch('/{inventory_id}', response_model=schemas.Inventory)
def update_inventory(inventory_id, inventory_item: schemas.InventoryUpdate, db: Session = Depends(get_db)):
    inventory_item_db = db.query(models.Inventory).filter(models.Inventory.inventory_id == inventory_id).first()
    if inventory_item_db is None:
        raise HTTPException(status_code=404, detail='Inventory item not found')
    
    for key, value in inventory_item.model_dump(exclude_unset=True).items():
        setattr(inventory_item_db, key, value)

    db.commit()
    db.refresh(inventory_item_db)    
    return inventory_item


@router.delete('/{inventory_id}')
def remove_inventory_item(inventory_id, db: Session = Depends(get_db)):
    inventory_item = db.query(models.Inventory).filter(models.Inventory.inventory_id == inventory_id).first()
    if inventory_item is None:
        raise HTTPException(status_code=404, detail='Product not found')
    
    db.delete(inventory_item)
    db.commit()
    return { "message": f"Inventory item with {inventory_item.inventory_id} deleted successfully" }
