from typing import List, Union, Optional
from pydantic import BaseModel, Field
from fastapi import Query
from datetime import datetime

class RegisterUserRequest(BaseModel):
    name: str
    surname: str
    age: int

class UserModel(BaseModel):
    id: int = Field(1)
    name: str = Field("Bob")
    surname: str = Field("Johnson")
    age: int = Field(27)

    class Config:
        orm_mode = True

class BasePicnicModel(BaseModel):
    id: int = Field(1)
    city: str = Field("Tyumen")
    time: datetime = Field(...)

class CreatePicnicModel(BaseModel):
    city_id: int = Field(Query(..., example=1))
    time: datetime = Field(Query(..., description='Время пикника'))

class GetPicnicsModel(BaseModel):
    time: Optional[datetime] = Field(Query(None, description='Время пикника (по умолчанию не задано)'))
    past: Optional[bool] = Field(Query(None, example=True, description='Включая уже прошедшие пикники'))
    
class UsersPicnicModel(BasePicnicModel):
    users: Union[List[UserModel], None] = None

class UserPicnicModel(BasePicnicModel):
    name: str = Field("Bob")

