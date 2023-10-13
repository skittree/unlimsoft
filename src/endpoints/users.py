from fastapi import HTTPException, Query, APIRouter
from external_requests import CheckCityExisting
from database import engine, Session, Base, User
from models import RegisterUserRequest, UserModel

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

@router.get('/users-list/', summary='')
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

@router.post('/register-user/', summary='CreateUser', response_model=UserModel)
def register_user(user: RegisterUserRequest):
    """
    Регистрация пользователя
    """
    user_object = User(**user.dict())
    s = Session()
    s.add(user_object)
    s.commit()

    return UserModel.from_orm(user_object)