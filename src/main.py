from fastapi import FastAPI, APIRouter
from fastapi.logger import logger
import logging

from routers import cities, picnics, users

app = FastAPI()
mainrouter = APIRouter(
    prefix="/api",
    responses={404: {"description": "Not found"}},
)

mainrouter.include_router(cities.router)
mainrouter.include_router(picnics.router)
mainrouter.include_router(users.router)
app.include_router(mainrouter)