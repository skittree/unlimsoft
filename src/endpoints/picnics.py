from fastapi import HTTPException, Query, APIRouter
import datetime as dt
from database import engine, Session, Base, Picnic, PicnicRegistration, City

router = APIRouter(
    prefix="/picnics",
    tags=["Picnics"],
    responses={404: {"description": "Not found"}},
)

@router.get('/all-picnics/', summary='All Picnics')
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

@router.post('/picnic-add/', summary='Picnic Add')
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

@router.post('/picnic-register/', summary='Picnic Registration')
def register_to_picnic(*_, **__,):
    """
    Регистрация пользователя на пикник
    """
    # TODO: Сделать логику
    return ...