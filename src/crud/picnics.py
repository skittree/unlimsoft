from db import Session, Picnic, PicnicRegistration, City, User
from models.picnics import GetPicnicsModel, CreatePicnicModel, CreatePicnicUser
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
import datetime as dt

# можно добавить кастомные exception'ы и ловить их вместо стандартного HTTPException

def get_list(model: GetPicnicsModel):
    picnics = Session().query(Picnic).join(Picnic.city)
    if model.time is not None:
        picnics = picnics.filter(Picnic.time == model.time)
    if not model.past:
        picnics = picnics.filter(Picnic.time >= dt.datetime.now())
    picnics = picnics.options(joinedload(Picnic.users)).all()

    return picnics

def create(model: CreatePicnicModel):
    s = Session()
    city = s.query(City).filter(City.id == model.city_id).first()
    if city is None:
        raise HTTPException(status_code=404, detail='Город с указанным city_id не существует')
    
    picnic = Picnic(city_id=model.city_id, time=model.time, city=city)
    
    s.add(picnic)
    s.commit()

    return picnic

def register_user(model: CreatePicnicUser):
    s = Session()
    picnic = s.query(Picnic).join(Picnic.city).filter(Picnic.id == model.picnic_id).first()
    if picnic is None:
        raise HTTPException(status_code=404, detail='Пикника с указанным picnic_id не существует')
    
    user = s.query(User).filter(User.id == model.user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='Пользователя с указанным user_id не существует')

    existing_registration = s.query(PicnicRegistration).filter(PicnicRegistration.user_id == model.user_id, PicnicRegistration.picnic_id == model.picnic_id).first()
    if existing_registration is not None:
        raise HTTPException(status_code=409, detail='Пользователь уже зарегистрирован на этот пикник')
    
    pr = PicnicRegistration(user_id=model.user_id, picnic_id=model.picnic_id)

    s.add(pr)
    s.commit()

    return picnic, user