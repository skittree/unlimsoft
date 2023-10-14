from typing import List
from fastapi import APIRouter, Depends
from pydantic import parse_obj_as

import crud
from db import get_session
from models.users import GetUsersModel, CreateUserModel, BaseUserModel

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

@router.get('/', summary='Users List', response_model=List[BaseUserModel])
def get_users(model: GetUsersModel = Depends(), session = Depends(get_session)) -> List[BaseUserModel]:
    """
    Список пользователей
    """
    users = crud.users.get_list(session, model)
    return parse_obj_as(List[BaseUserModel], users)

@router.post('/', summary='Create User', response_model=BaseUserModel)
def create_user(model: CreateUserModel, session = Depends(get_session)) -> BaseUserModel:
    """
    Регистрация пользователя
    """
    user = crud.users.create(session, model)
    return BaseUserModel.from_orm(user)