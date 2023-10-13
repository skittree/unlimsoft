from typing import List
from fastapi import HTTPException, Query, APIRouter, Depends
from pydantic import parse_obj_as
from database import engine, Session, Base, City
from external_requests import GetWeatherRequest
from models import BaseCityModel, CreateCityModel, GetCityModel

router = APIRouter(
    prefix="/cities",
    tags=["Cities"],
    responses={404: {"description": "Not found"}},
)

@router.post('/', summary='Create City', response_model=BaseCityModel)
def create_city(model: CreateCityModel = Depends()) -> BaseCityModel:
    """
    Создание города по его названию
    """
    weather = GetWeatherRequest().get_weather(model.name)
    if not weather:
        raise HTTPException(status_code=400, detail='Параметр name должен быть существующим городом')
    
    s = Session()
    city_object = s.query(City).filter(City.name == model.name.capitalize()).first()
    if city_object is None:
        city_object = City(name=model.name.capitalize())
        s.add(city_object)
        s.commit()

    return BaseCityModel.from_orm(city_object)

@router.get('/', summary='Get Cities', response_model=List[BaseCityModel])
def cities_list(model: GetCityModel = Depends()) -> List[BaseCityModel]:
    """
    Получение списка городов
    """
    query = Session().query(City)
    
    if model.name is not None:
        query = query.filter(City.name == model.name.capitalize())
    
    cities = query.all()

    return parse_obj_as(List[BaseCityModel], cities)