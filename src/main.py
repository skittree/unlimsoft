from fastapi import FastAPI, HTTPException, Query

from routers import cities, picnics, users

app = FastAPI(prefix='/api')
app.include_router(cities.router)
app.include_router(picnics.router)
app.include_router(users.router)