from fastapi import APIRouter
from api.v1 import film, genre, person

api = APIRouter()

api.include_router(film.router, prefix='/v1/films', tags=['film'])
api.include_router(genre.router, prefix='/v1/genres', tags=['genre'])
api.include_router(person.router, prefix='/v1/persons', tags=['person'])

