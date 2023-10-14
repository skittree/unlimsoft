# Сюда написать тесты
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from external_requests import GetWeatherRequest
from database import Base

# Создание сессии
DATABASE_URL = "sqlite:///test.db"
engine = create_engine(DATABASE_URL)
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)



Base.metadata.create_all(bind=engine)