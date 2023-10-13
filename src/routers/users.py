from typing import List
from fastapi import HTTPException, Query, APIRouter, Depends
from pydantic import parse_obj_as
from database import engine, Session, Base, User
from models import GetUsersModel, RegisterUserRequest, UserModel

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

@router.get('/', summary='Users List', response_model=List[UserModel])
def users_list(model: GetUsersModel = Depends()) -> List[UserModel]:
    """
    Список пользователей
    """
    users = Session().query(User)
    if model.min_age is not None:
        users = users.filter(User.age >= model.min_age)
    if model.max_age is not None:
        users = users.filter(User.age <= model.max_age)

    users = users.all()

    return parse_obj_as(List[UserModel], users)

@router.post('/', summary='Create User', response_model=UserModel)
def register_user(user: RegisterUserRequest):
    """
    Регистрация пользователя
    """
    user_object = User(**user.dict())
    s = Session()
    s.add(user_object)
    s.commit()

    return UserModel.from_orm(user_object)