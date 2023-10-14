from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db import Base

class User(Base):
    """
    Пользователь
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    age = Column(Integer, nullable=True)

    picnics = relationship('Picnic', secondary='picnic_registration', back_populates='users')

    def __repr__(self):
        return f'<Пользователь {self.surname} {self.name}>'