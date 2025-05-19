from app.db.base import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(length=255), nullable=False, index=True)
    description = Column(String(length=500), nullable=True)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # inventory = relationship('Inventory', back_populates="product", uselist=False)
    # sales = relationship("Sale", back_populates="product")


class Inventory(Base):
    __tablename__ = 'inventory'
    inventory_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), unique=True, nullable=False)
    in_stock = Column(Integer, nullable=False, default=0)
    last_updated = Column(DateTime, onupdate=func.now())

    # product = relationship('Product', back_populates="inventory")


class Sale(Base):
    __tablename__ = 'sales'
    sale_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    sale_price = Column(Float, nullable=False)
    sale_date = Column(DateTime, default=func.now(), index=True)

    # product = relationship("Product", back_populates="sales")
