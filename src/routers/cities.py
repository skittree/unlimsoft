from typing import List
from fastapi import APIRouter, Depends
from pydantic import parse_obj_as

import crud
from db import Session
from models.cities import BaseCityModel, CreateCityModel, GetCityModel

router = APIRouter(
    prefix="/cities",
    tags=["Cities"],
    responses={404: {"description": "Not found"}},
)

@router.get('/', summary='Get Cities', response_model=List[BaseCityModel])
def get_cities(model: GetCityModel = Depends()) -> List[BaseCityModel]:
    """
    Получение списка городов
    """
    session = Session()
    cities = crud.cities.get_list(session, model)
    return parse_obj_as(List[BaseCityModel], cities)

@router.post('/', summary='Create City', response_model=BaseCityModel)
def create_city(model: CreateCityModel = Depends()) -> BaseCityModel:
    """
    Создание города по его названию
    """
    session = Session()
    city_object = crud.cities.create(session, model)
    return BaseCityModel.from_orm(city_object)