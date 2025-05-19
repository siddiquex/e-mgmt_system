from fastapi import FastAPI
from app.routes import inventory, products, sales
from app.db.base import Base
from app.db.session import Session, engine
from app.populate_db import init_db_and_tables, populate_database_if_empty


app = FastAPI()

# populate db
init_db_and_tables(engine, Base)
populate_database_if_empty(Session)

# integrates seggregated routes
app.include_router(inventory.router)
app.include_router(products.router)
app.include_router(sales.router)

@app.get('/')
def root():
    return { "message": "Hello from BE" }
