from fastapi import HTTPException, Query, APIRouter
from database import engine, Session, Base, City
from external_requests import CheckCityExisting

router = APIRouter(
    prefix="/cities",
    tags=["Cities"],
    responses={404: {"description": "Not found"}},
)

@router.post('/create-city/', summary='Create City', description='Создание города по его названию')
def create_city(city: str = Query(description="Название города", default=None)):
    if city is None:
        raise HTTPException(status_code=400, detail='Параметр city должен быть указан')
    check = CheckCityExisting()
    if not check.check_existing(city):
        raise HTTPException(status_code=400, detail='Параметр city должен быть существующим городом')

    city_object = Session().query(City).filter(City.name == city.capitalize()).first() # что если набрать город с нижним реестром?
    if city_object is None:
        city_object = City(name=city.capitalize())
        s = Session()
        s.add(city_object)
        s.commit()

    return {'id': city_object.id, 'name': city_object.name, 'weather': city_object.weather} # почему не возвращаем/принимаем pydantic модели?

@router.get('/get-cities/', summary='Get Cities', description='Получение списка городов или города по названию')
def cities_list(q: str = Query(description="Название города", default=None)):
    """
    Получение списка городов
    """
    query = Session().query(City)
    
    if q is not None:
        query = query.filter(City.name == q.capitalize())
    
    cities = query.all()

    return [{'id': city.id, 'name': city.name, 'weather': city.weather} for city in cities]