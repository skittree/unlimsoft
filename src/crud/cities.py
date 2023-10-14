from db import City
from models.cities import GetCityModel, CreateCityModel
from ext.external_requests import GetWeatherRequest
from fastapi import HTTPException

# можно добавить кастомные exception'ы и ловить их вместо стандартного HTTPException

def get_list(session, model: GetCityModel):
    query = session.query(City)
    
    if model.name is not None:
        query = query.filter(City.name == model.name.capitalize())
    
    cities = query.all()
    return cities

def create(session, model: CreateCityModel):
    check = GetWeatherRequest()
    if not check.get_weather(model.name):
        raise HTTPException(status_code=404, detail='Параметр name должен быть существующим городом')

    city_object = session.query(City).filter(City.name == model.name.capitalize()).first()
    if city_object is None:
        city_object = City(name=model.name.capitalize())
        session.add(city_object)
        session.commit()

    return city_object