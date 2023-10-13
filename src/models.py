from typing import List, Union, Optional
from pydantic import BaseModel, Field
from fastapi import Query, Path
from datetime import datetime

# users

class GetUsersModel(BaseModel):
    min_age: Optional[int] = Field(Query(None, example=18, description='Минимальный возраст'))
    max_age: Optional[int] = Field(Query(None, example=65, description='Максимальный возраст'))

class RegisterUserRequest(BaseModel):
    name: str = Field("Bob")
    surname: str = Field("Johnson")
    age: int = Field(27)

class UserModel(BaseModel):
    id: int = Field(1)
    name: str = Field("Bob")
    surname: str = Field("Johnson")
    age: int = Field(27)

    class Config:
        orm_mode = True

# picnics

class BasePicnicModel(BaseModel):
    id: int = Field(1)
    city: str = Field("Tyumen")
    time: datetime = Field(...)

class CreatePicnicModel(BaseModel):
    city_id: int = Field(Query(..., example=1, description='ID города'))
    time: datetime = Field(Query(..., description='Время пикника'))

class GetPicnicsModel(BaseModel):
    time: Optional[datetime] = Field(Query(None, description='Время пикника (по умолчанию не задано)'))
    past: Optional[bool] = Field(Query(None, example=True, description='Включая уже прошедшие пикники'))
    
class UsersPicnicModel(BasePicnicModel):
    users: Union[List[UserModel], None] = None

class UserPicnicModel(BasePicnicModel):
    name: str = Field("Bob")

class RegisterUserPicnicRequest(BaseModel):
    picnic_id: int = Field(Path(..., example=1, description='ID пикника'))
    user_id: int = Field(Query(..., example=1, description='ID пользователя'))

# cities

class CreateCityModel(BaseModel):
    name: str = Field(Query(..., example="Tyumen", description="Название города"))

class GetCityModel(BaseModel):
    name: Optional[str] = Field(Query(None, description="Название города"))

class BaseCityModel(BaseModel):
    id: int = Field(1)
    name: str = Field("Tyumen")
    weather: float = Field(20.55)

    class Config:
        orm_mode = True