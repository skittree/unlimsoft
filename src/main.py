import datetime as dt
from fastapi import FastAPI, HTTPException, Query
from database import engine, Session, Base, City, User, Picnic, PicnicRegistration
from external_requests import CheckCityExisting, GetWeatherRequest
from models import RegisterUserRequest, UserModel

app = FastAPI()


@app.post('/create-city/', summary='Create City', description='Создание города по его названию')
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


@app.get('/get-cities/', summary='Get Cities', description='Получение списка городов или города по названию')
def cities_list(q: str = Query(description="Название города", default=None)):
    """
    Получение списка городов
    """
    query = Session().query(City)
    
    if q is not None:
        query = query.filter(City.name == q.capitalize())
    
    cities = query.all()

    return [{'id': city.id, 'name': city.name, 'weather': city.weather} for city in cities]


@app.get('/users-list/', summary='')
def users_list(minage: int = Query(description="Минимальный возраст", default=None),
               maxage: int = Query(description="Максимальный возраст", default=None)):
    """
    Список пользователей
    """
    users = Session().query(User)
    if minage is not None:
        users = users.filter(User.age >= minage)
    if maxage is not None:
        users = users.filter(User.age <= maxage)

    users = users.all()

    return [{
        'id': user.id,
        'name': user.name,
        'surname': user.surname,
        'age': user.age,
    } for user in users]


@app.post('/register-user/', summary='CreateUser', response_model=UserModel)
def register_user(user: RegisterUserRequest):
    """
    Регистрация пользователя
    """
    user_object = User(**user.dict())
    s = Session()
    s.add(user_object)
    s.commit()

    return UserModel.from_orm(user_object)


@app.get('/all-picnics/', summary='All Picnics', tags=['picnic'])
def all_picnics(datetime: dt.datetime = Query(default=None, description='Время пикника (по умолчанию не задано)'),
                past: bool = Query(default=True, description='Включая уже прошедшие пикники')):
    """
    Список всех пикников
    """
    picnics = Session().query(Picnic)
    if datetime is not None:
        picnics = picnics.filter(Picnic.time == datetime)
    if not past:
        picnics = picnics.filter(Picnic.time >= dt.datetime.now())

    return [{
        'id': pic.id,
        'city': Session().query(City).filter(City.id == pic.id).first().name,
        'time': pic.time,
        'users': [
            {
                'id': pr.user.id,
                'name': pr.user.name,
                'surname': pr.user.surname,
                'age': pr.user.age,
            }
            for pr in Session().query(PicnicRegistration).filter(PicnicRegistration.picnic_id == pic.id)],
    } for pic in picnics]


@app.post('/picnic-add/', summary='Picnic Add', tags=['picnic'])
def picnic_add(city_id: int = Query(default=None, description='ID города'), 
               datetime: dt.datetime = Query(default=None, description='Время провождения пикника')):
    city = Session().query(City).filter(City.id == city_id).first()
    if city is None:
        raise HTTPException(status_code=400, detail='Города с указанным city_id не существует')
    
    p = Picnic(city_id=city_id, time=datetime)
    s = Session()
    s.add(p)
    s.commit()

    return {
        'id': p.id,
        'city': city.name,
        'time': p.time,
    }


@app.post('/picnic-register/', summary='Picnic Registration', tags=['picnic'])
def register_to_picnic(*_, **__,):
    """
    Регистрация пользователя на пикник
    """
    # TODO: Сделать логику
    return ...

