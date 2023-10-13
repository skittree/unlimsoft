from typing import List
from fastapi import HTTPException, Query, APIRouter, Depends
from pydantic import parse_obj_as
from database import engine, Session, Base, User
from models import GetUsersModel, CreateUserModel, BaseUserModel

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

@router.get('/', summary='Users List', response_model=List[BaseUserModel])
def get_users(model: GetUsersModel = Depends()) -> List[BaseUserModel]:
    """
    Список пользователей
    """
    users = Session().query(User)
    if model.min_age is not None:
        users = users.filter(User.age >= model.min_age)
    if model.max_age is not None:
        users = users.filter(User.age <= model.max_age)

    users = users.all()

    return parse_obj_as(List[BaseUserModel], users)

@router.post('/', summary='Create User', response_model=BaseUserModel)
def create_user(user: CreateUserModel) -> BaseUserModel:
    """
    Регистрация пользователя
    """
    user_object = User(**user.dict())
    s = Session()
    s.add(user_object)
    s.commit()

    return BaseUserModel.from_orm(user_object)