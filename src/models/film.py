from typing import Optional, List, Union
from models.base import ORJSONModel
from pydantic import Field

class Person(ORJSONModel):
    id: str
    name: str


class FullFilm(ORJSONModel):
    id: str
    imdb_rating: Union[float, list] = 0
    genre: Optional[List[str]] = []
    title: str
    description: Union[str, list] = []
    director: Optional[List[str]] = []
    actors_names: Optional[List[str]] = []
    writers_names: Optional[List[str]] = Field(default_factory=list)


class ShortFilm(ORJSONModel):
    id: str
    imdb_rating: Union[float, list] = 0
    genre: Optional[List[str]] = []
    title: str
