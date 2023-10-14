from typing import List
from fastapi import APIRouter, Depends
from pydantic import parse_obj_as

import crud
from models.picnics import CreatePicnicModel, GetPicnicsModel, BasePicnicModel, CreatePicnicUser, PicnicUsersModel, PicnicUserModel
from models.users import BaseUserModel

router = APIRouter(
    prefix="/picnics",
    tags=["Picnics"],
    responses={404: {"description": "Not found"}},
)

@router.get('/', summary='Picnics List', response_model=List[PicnicUsersModel])
def get_picnics(model: GetPicnicsModel = Depends()) -> List[PicnicUsersModel]:
    """
    Список всех пикников
    """
    picnics = crud.picnics.get_list(model)
    output = [PicnicUsersModel(id=picnic.id, 
                               city=picnic.city.name, 
                               time=picnic.time, 
                               users=parse_obj_as(List[BaseUserModel], 
                               picnic.users)) for picnic in picnics]
    return output

@router.post('/', summary='Create Picnic', response_model=BasePicnicModel)
def create_picnic(model: CreatePicnicModel = Depends()) -> BasePicnicModel:
    """
    Создать пикник
    """
    picnic = crud.picnics.create(model)
    return BasePicnicModel(
        id=picnic.id,
        city=picnic.city.name,
        time=picnic.time
    )

@router.post('/{picnic_id}/register', summary='Picnic Registration', response_model=PicnicUserModel)
def register_to_picnic(model: CreatePicnicUser = Depends()) -> PicnicUserModel:
    """
    Регистрация пользователя на пикник
    """
    picnic, user = crud.picnics.register_user(model)
    return PicnicUserModel(
        id = picnic.id,
        city = picnic.city.name,
        time = picnic.time,
        name = user.name
    )