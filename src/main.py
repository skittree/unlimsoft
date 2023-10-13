import datetime as dt
from fastapi import FastAPI, HTTPException, Query
from database import engine, Session, Base, City, User, Picnic, PicnicRegistration

from endpoints import cities, picnics, users

app = FastAPI()
app.include_router(cities.router)
app.include_router(picnics.router)
app.include_router(users.router)