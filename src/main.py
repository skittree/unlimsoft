from fastapi import FastAPI, APIRouter
from routers import cities, picnics, users
import logging

logger = logging.getLogger(__name__)

app = FastAPI()
main_router = APIRouter(
    prefix="/api",
    responses={404: {"description": "Not found"}},
)

main_router.include_router(cities.router)
main_router.include_router(picnics.router)
main_router.include_router(users.router)

app.include_router(main_router)