from typing import Optional
from pydantic import BaseModel, Field
from fastapi import Query

class BaseUserModel(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example="Bob")
    surname: str = Field(example="Johnson")
    age: int = Field(example=27)

    class Config:
        orm_mode = True

class GetUsersModel(BaseModel):
    min_age: Optional[int] = Field(Query(None, example=18, description='Минимальный возраст'))
    max_age: Optional[int] = Field(Query(None, example=65, description='Максимальный возраст'))

class CreateUserModel(BaseModel):
    name: str = Field(..., example="Bob")
    surname: str = Field(..., example="Johnson")
    age: int = Field(..., example=27)