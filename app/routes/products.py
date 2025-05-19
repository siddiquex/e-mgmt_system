from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.db import get_db
from app import models, schemas
from typing import List


router = APIRouter(
        prefix='/products',
        tags=['Products'],
        responses={404: {"description": "Not found"}}
    )

@router.post('/', response_model=schemas.Product)
def add_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    new_product = models.Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.get('/', response_model=List[schemas.Product])
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products


@router.get('/{product_id}', response_model=schemas.Product)
def get_product(product_id, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.product_id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail='Product not found')
    return product


@router.patch('/{product_id}', response_model=schemas.Product)
def update_product(product_id, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    product_db = db.query(models.Product).filter(models.Product.product_id == product_id).first()
    if product_db is None:
        raise HTTPException(status_code=404, detail='Product not found')
    
    for key, value in product.model_dump(exclude_unset=True).items():
        setattr(product_db, key, value)
    
    db.commit()
    db.refresh(product)
    return product


@router.delete('/{product_id}')
def remove_product(product_id, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.product_id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail='Product not found')
    
    db.delete(product)
    db.commit()
    return { "message": f"Product with {product.product_id} deleted successfully" }
