from typing import List, Union, Optional
from pydantic import BaseModel, Field
from fastapi import Query, Path
from datetime import datetime as dt
from .users import BaseUserModel

class BasePicnicModel(BaseModel):
    id: int = Field(example=1)
    city: str = Field(example="Tyumen")
    time: dt = Field(default_factory = dt.now)

class CreatePicnicModel(BaseModel):
    city_id: int = Field(Query(..., example=1, description='ID города'))
    time: dt = Field(Query(..., default_factory = dt.now, description='Время пикника'))

class GetPicnicsModel(BaseModel):
    time: Optional[dt] = Field(Query(None, description='Время пикника (по умолчанию не задано)'))
    past: Optional[bool] = Field(Query(None, example=True, description='Включая уже прошедшие пикники'))
    
class PicnicUsersModel(BasePicnicModel):
    users: Union[List[BaseUserModel], None] = None

class PicnicUserModel(BasePicnicModel):
    name: str = Field(example="Bob")

class CreatePicnicUser(BaseModel):
    picnic_id: int = Field(Path(..., example=1, description='ID пикника'))
    user_id: int = Field(Query(..., example=1, description='ID пользователя'))