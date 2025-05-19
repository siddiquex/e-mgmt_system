
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DB_URL = os.environ.get('DB_URL')
print('DB_URL', DB_URL)

engine = create_engine(DB_URL)
Session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
