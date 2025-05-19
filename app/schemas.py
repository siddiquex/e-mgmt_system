from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

# Product schemas
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


class Product(BaseSchema, ProductBase):
    product_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    # inventory: Optional["Inventory"] = None
    # sales: Optional[List["Sale"]] = None

# Inventory schemas
class InventoryBase(BaseModel):
    in_stock: int
    product_id: int

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(InventoryBase):
    in_stock: int

class Inventory(BaseSchema, InventoryBase):
    inventory_id: int
    last_updated: datetime
    # product: Optional["Product"] = None

# Sale schemas
class SaleBase(BaseModel):
    quantity: int
    sale_price: float
    product_id: int

class SaleCreate(SaleBase):
    pass

class SaleUpdate(SaleBase):
    quantity: Optional[int] = None
    sale_price: Optional[float] = None

class Sale(BaseSchema, SaleBase):
    sale_id: int
    sale_date: datetime
    # product: Optional["Product"] = None


class DailyRevenue(BaseModel):
    sale_date: datetime
    daily_revenue: float


class WeeklyRevenue(BaseModel):
    week_start: datetime
    weekly_revenue: float

class MonthlyRevenue(BaseModel):
    month_start: datetime
    monthly_revenue: float

class AnnualRevenue(BaseModel):
    year: int
    annual_revenue: float
