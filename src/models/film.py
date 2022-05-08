from typing import Optional, List, Union
from models.base import ORJSONModel
from models.genre import Genre



class FullFilm(ORJSONModel):
    id: str
    imdb_rating: Union[float, list] = 0
    genre: Optional[List[Genre]]
    title: str
    description: Union[str, list, None] = []
    director: Optional[List[str]] = []
    actors_names: Optional[List[str]] = []
    writers_names: Optional[List[str]] = []


class ShortFilm(ORJSONModel):
    id: str
    imdb_rating: Optional[Union[float, list]]
    genre: Optional[List[Genre]]
    title: str
