from db import Session, City
from models.cities import GetCityModel, CreateCityModel
from ext.external_requests import GetWeatherRequest
from fastapi import HTTPException

# можно добавить кастомные exception'ы и ловить их вместо стандартного HTTPException

def get_list(model: GetCityModel):
    query = Session().query(City)
    
    if model.name is not None:
        query = query.filter(City.name == model.name.capitalize())
    
    cities = query.all()
    return cities

def create(model: CreateCityModel):
    check = GetWeatherRequest()
    if not check.get_weather(model.name):
        raise HTTPException(status_code=404, detail='Параметр name должен быть существующим городом')
    
    s = Session()
    city_object = s.query(City).filter(City.name == model.name.capitalize()).first()
    if city_object is None:
        city_object = City(name=model.name.capitalize())
        s.add(city_object)
        s.commit()

    return city_object