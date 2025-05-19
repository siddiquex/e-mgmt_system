from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.db.db import get_db
from app import models, schemas
from typing import List, Optional
from datetime import datetime

router = APIRouter(
        prefix='/sales',
        tags=['Sales'],
        responses={404: {"description": "Not found"}}
    )


@router.post('/', response_model=schemas.Sale)
def add_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    new_sale = models.Sale(**sale.model_dump())
    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)
    return new_sale


@router.get('/', response_model=List[schemas.Sale])
def get_sales(
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    product_id: Optional[int] = None,
):
    query = db.query(models.Sale)

    if start_date:
        query = query.filter(models.Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(models.Sale.sale_date <= end_date)
    if product_id:
        query = query.filter(models.Sale.product_id == product_id)

    sales = query.all()
    return sales


@router.get('/{sale_id}', response_model=schemas.Sale)
def get_sale(sale_id, db: Session = Depends(get_db)):
    sale = db.query(models.Sale).filter(models.Sale.sale_id == sale_id).first()
    if sale is None:
        raise HTTPException(status_code=404, detail='Sale not found')
    return 


@router.patch('/{sale_id}', response_model=schemas.Sale)
def update_sale(sale_id, sale_update: schemas.SaleUpdate, db: Session = Depends(get_db)):
    sale_db = db.query(models.Sale).filter(models.Sale.sale_id == sale_id).first()
    if sale_db is None:
        raise HTTPException(status_code=404, detail='Sale not found')
    
    for key, value in sale_update.model_dump(exclude_unset=True).items():
        setattr(sale_db, key, value)
    
    db.commit()
    db.refresh(sale_db)
    return sale_update


@router.delete('/{sale_id}')
def remove_product(sale_id, db: Session = Depends(get_db)):
    sale = db.query(models.Sale).filter(models.Sale.sale_id == sale_id).first()
    if sale is None:
        raise HTTPException(status_code=404, detail='Sale not found')
    
    db.delete(sale)
    db.commit()
    return { "message": f"Sale with {sale.sale_id} deleted successfully" }


@router.get("/daily_revenue", response_model=List[schemas.DailyRevenue])
def get_daily_revenue(
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    product_id: Optional[int] = None,
):
    query = (
        db.query(
            func.date(models.Sale.sale_date).label("sale_date"),
            func.sum(models.Sale.sale_price * models.Sale.quantity).label("daily_revenue"),
        )
        .group_by("sale_date")
        .order_by("sale_date")
    )

    if start_date:
        query = query.filter(models.Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(models.Sale.sale_date <= end_date)
    if product_id:
        query = query.filter(models.Sale.product_id == product_id)

    results = query.all()
    return results


@router.get("/weekly_revenue", response_model=List[schemas.WeeklyRevenue])
def get_weekly_revenue(
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    product_id: Optional[int] = None,

):
    query = (
        db.query(
            func.date_trunc("week", models.Sale.sale_date).label("week_start"),
            func.sum(models.Sale.sale_price * models.Sale.quantity).label("weekly_revenue"),
        )
        .group_by("week_start")
        .order_by("week_start")
    )

    if start_date:
        query = query.filter(models.Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(models.Sale.sale_date <= end_date)
    if product_id:
        query = query.filter(models.Sale.product_id == product_id)

    results = query.all()
    return results


@router.get("/monthly_revenue", response_model=List[schemas.MonthlyRevenue])
def get_monthly_revenue(
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    product_id: Optional[int] = None,
):
    query = (
        db.query(
            func.date_trunc("month", models.Sale.sale_date).label("month_start"),
            func.sum(models.Sale.sale_price * models.Sale.quantity).label("monthly_revenue"),
        )
        .group_by("month_start")
        .order_by("month_start")
    )

    if start_date:
        query = query.filter(models.Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(models.Sale.sale_date <= end_date)
    if product_id:
        query = query.filter(models.Sale.product_id == product_id)

    results = query.all()
    return results


@router.get("/annual_revenue", response_model=List[schemas.AnnualRevenue])
def get_annual_revenue(
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    product_id: Optional[int] = None,
):
    query = (
        db.query(
            func.extract("year", models.Sale.sale_date).label("year"),
            func.sum(models.Sale.sale_price * models.Sale.quantity).label("annual_revenue"),
        )
        .group_by("year")
        .order_by("year")
    )

    if start_date:
        query = query.filter(models.Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(models.Sale.sale_date <= end_date)
    if product_id:
        query = query.filter(models.Sale.product_id == product_id)

    results = query.all()
    return results
