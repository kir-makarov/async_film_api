from pydantic import BaseModel
from typing import Optional, List, Union


class Person(BaseModel):
    id: str
    name: str


class FullFilm(BaseModel):
    id: str
    imdb_rating: Union[float, list] = 0
    genre: Optional[List[str]] = []
    title: str
    description: Union[str, list]
    director: List[str] = []
    actors_names: List = []
    writers_names: List = []


class ShortFilm(BaseModel):
    id: str
    imdb_rating: Union[float, list] = 0
    genre: Optional[List[str]] = []
    title: str


class QueryFilms(BaseModel):
    q: Optional[str]
    sort: Optional[str]

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))
