from typing import Optional
from pydantic import BaseModel, Field
from fastapi import Query

class BaseCityModel(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example="Tyumen")
    weather: float = Field(example=20.55)

    class Config:
        orm_mode = True

class CreateCityModel(BaseModel):
    name: str = Field(Query(..., example="Tyumen", description="Название города"))

class GetCityModel(BaseModel):
    name: Optional[str] = Field(Query(None, description="Название города"))