from typing import List
from fastapi import HTTPException, Query, APIRouter, Depends
from pydantic import parse_obj_as
from sqlalchemy.orm import joinedload
from database import engine, Session, Base, Picnic, PicnicRegistration, City, User
import datetime as dt
from models import CreatePicnicModel, GetPicnicsModel, BasePicnicModel, UsersPicnicModel, UserPicnicModel, UserModel

router = APIRouter(
    prefix="/picnics",
    tags=["Picnics"],
    responses={404: {"description": "Not found"}},
)

@router.get('/', summary='Picnics List', response_model=List[UsersPicnicModel])
def get_picnics(model: GetPicnicsModel = Depends()) -> List[UsersPicnicModel]:
    """
    Список всех пикников
    """
    picnics = Session().query(Picnic).join(Picnic.city)
    if model.time is not None:
        picnics = picnics.filter(Picnic.time == model.time)
    if not model.past:
        picnics = picnics.filter(Picnic.time >= dt.datetime.now())
    picnics = picnics.options(joinedload(Picnic.users)).all()

    output = [UsersPicnicModel(
                id=picnic.id,
                city=picnic.city.name,
                time=picnic.time,
                users=parse_obj_as(List[UserModel], picnic.users)
            ) for picnic in picnics]
        
    return output

@router.post('/', summary='Create Picnic', response_model=BasePicnicModel)
def create_picnic(model: CreatePicnicModel = Depends()) -> BasePicnicModel:
    """
    Создать пикник
    """
    s = Session()
    city = s.query(City).filter(City.id == model.city_id).first()
    if city is None:
        raise HTTPException(status_code=400, detail='Город с указанным city_id не существует')
    
    p = Picnic(city_id=model.city_id, time=model.time)
    
    s.add(p)
    s.commit()

    return BasePicnicModel(
        id=p.id,
        city=city.name,
        time=p.time
    )

@router.post('/{picnic_id}/register', summary='Picnic Registration', response_model=UserPicnicModel)
def register_to_picnic(picnic_id: int, user_id: int = Query(..., description='ID пользователя')) -> UserPicnicModel:
    """
    Регистрация пользователя на пикник
    """
    s = Session()
    picnic = s.query(Picnic).join(Picnic.city).filter(Picnic.id == picnic_id).first()
    if picnic is None:
        raise HTTPException(status_code=400, detail='Пикника с указанным picnic_id не существует')
    
    user = s.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=400, detail='Пользователя с указанным user_id не существует')

    existing_registration = s.query(PicnicRegistration).filter(PicnicRegistration.user_id == user_id, PicnicRegistration.picnic_id == picnic_id).first()
    if existing_registration is not None:
        raise HTTPException(status_code=400, detail='Пользователь уже зарегистрирован на этот пикник')
    
    pr = PicnicRegistration(user_id=user_id, picnic_id=picnic_id)

    s.add(pr)
    s.commit()
    
    return UserPicnicModel(
        id = picnic.id,
        city = picnic.city.name,
        time = picnic.time,
        name = user.name
    )