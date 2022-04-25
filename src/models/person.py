from pydantic import BaseModel
from typing import Optional


class ShortPerson(BaseModel):
    id: str
    full_name: str


class FullPerson(BaseModel):
    id: str
    full_name: str
    roles: Optional[list]
    film_ids: Optional[list]


class QueryPerson(BaseModel):

    q: Optional[str]

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))
