from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import text, Engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative  import declarative_base
from .models import Inventory, Product, Sale

def init_db_and_tables(engine: Engine, Base: declarative_base):
    # create db if it doesn't exist
    if not database_exists(engine.url):
        print(f"Databse doesn't exist, creating database {engine.url}")
        create_database(engine.url)
        print(f"Database created at {engine.url}")

    
    # create tables if they don't exist
    print("Creating tables if they don't exist")
    Base.metadata.create_all(bind=engine)


def populate_database_if_empty(Session: Session):
    db = Session()
    try:
        product_count = db.query(Product).count()
        inventory_count = db.query(Inventory).count()
        sale_count = db.query(Sale).count()

        # Populate db with the sample data only if the tables are empty
        if product_count == 0 and inventory_count == 0 and sale_count == 0:
            print("Tables are empty, populating with the sample data")
            products_sql_script = """
                INSERT INTO products (name, description, price, created_at, updated_at) VALUES
                    ('Smart Speaker with Voice Assistant', 'Voice-controlled smart speaker.', 49.99, NOW(), NULL),
                    ('Wireless Noise-Canceling Headphones', 'Over-ear wireless headphones with ANC.', 199.00, NOW(), NULL),
                    ('4K Ultra HD Smart Television', '55-inch smart TV with 4K resolution.', 799.99, NOW(), NULL),
                    ('Portable Bluetooth Speaker', 'Waterproof portable Bluetooth speaker.', 29.50, NOW(), NULL),
                    ('Fitness Tracker Wristband', 'Water-resistant fitness tracking band.', 35.00, NOW(), NULL),
                    ('Digital Kitchen Scale', 'High-precision digital kitchen scale.', 19.75, NOW(), NULL),
                    ('Electric Toothbrush with Timer', 'Rechargeable electric toothbrush.', 55.00, NOW(), NULL),
                    ('Coffee Maker with Grinder', 'Automatic coffee maker with built-in grinder.', 129.00, NOW(), NULL),
                    ('Gaming Mouse with RGB Lighting', 'Wired gaming mouse with customizable RGB.', 39.99, NOW(), NULL),
                    ('Ergonomic Office Chair', 'Adjustable ergonomic office chair.', 249.00, NOW(), NULL);
            """
            
            inventory_sql_script = """
                INSERT INTO inventory (product_id, in_stock, last_updated) VALUES
                    (1, 150, NOW()),
                    (2, 75, NOW()),
                    (3, 30, NOW()),
                    (4, 200, NOW()),
                    (5, 120, NOW()),
                    (6, 90, NOW()),
                    (7, 60, NOW()),
                    (8, 45, NOW()),
                    (9, 110, NOW()),
                    (10, 50, NOW());
            """

            sales_sql_script = """
                INSERT INTO sales (product_id, quantity, sale_price, sale_date) VALUES
                    (1, 2, 49.99, '2025-05-19 10:00:00'),
                    (3, 1, 799.99, '2025-05-19 10:15:00'),
                    (2, 1, 199.00, '2025-05-19 10:30:00'),
                    (1, 5, 47.50, '2025-05-19 11:00:00'),
                    (4, 3, 28.00, '2025-05-19 11:45:00'),
                    (7, 1, 55.00, '2025-05-19 12:00:00'),
                    (2, 2, 190.00, '2025-05-19 13:30:00'),
                    (9, 1, 39.99, '2025-05-19 14:00:00'),
                    (5, 1, 35.00, '2025-05-19 15:15:00'),
                    (3, 1, 780.00, '2025-05-19 16:45:00');
            """

        
            db.execute(text(products_sql_script))
            db.commit()

            db.execute(text(inventory_sql_script))
            db.commit()
            
            db.execute(text(sales_sql_script))
            db.commit()
            print("DB Populated successfully")
        else:
            print("Tables are not empty, skipping populating of DB")

    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.close()

