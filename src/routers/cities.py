from typing import List
from fastapi import APIRouter, Depends
from pydantic import parse_obj_as

import crud
from db import get_session
from models.cities import BaseCityModel, CreateCityModel, GetCityModel

router = APIRouter(
    prefix="/cities",
    tags=["Cities"],
    responses={404: {"description": "Not found"}},
)

@router.get('/', summary='Get Cities', response_model=List[BaseCityModel])
def get_cities(model: GetCityModel = Depends(), session = Depends(get_session)) -> List[BaseCityModel]:
    """
    Получение списка городов
    """
    cities = crud.cities.get_list(session, model)
    return parse_obj_as(List[BaseCityModel], cities)

@router.post('/', summary='Create City', response_model=BaseCityModel)
def create_city(model: CreateCityModel = Depends(), session = Depends(get_session)) -> BaseCityModel:
    """
    Создание города по его названию
    """
    city = crud.cities.create(session, model)
    return BaseCityModel.from_orm(city)