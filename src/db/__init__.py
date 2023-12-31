from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

# Создание сессии
engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)

def get_session():
    with Session() as session:
        yield session

Base = declarative_base()

from .cities import City
from .picnics import Picnic, PicnicRegistration
from .users import User

Base.metadata.create_all(bind=engine)