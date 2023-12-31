from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db import Base

class Picnic(Base):
    """
    Пикник
    """
    __tablename__ = 'picnic'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey('city.id'), nullable=False)
    time = Column(DateTime, nullable=False)

    city = relationship('City', back_populates='picnics')
    users = relationship('User', secondary='picnic_registration', back_populates='picnics')

    def __repr__(self):
        return f'<Пикник {self.id}>'

class PicnicRegistration(Base):
    """
    Регистрация пользователя на пикник
    """
    __tablename__ = 'picnic_registration'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    picnic_id = Column(Integer, ForeignKey('picnic.id'), nullable=False)

    def __repr__(self):
        return f'<Регистрация {self.id}>'