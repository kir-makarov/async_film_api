from models.base import ORJSONModel
from typing import Optional


class ShortPerson(ORJSONModel):
    id: str
    full_name: str


class FullPerson(ORJSONModel):
    id: str
    full_name: str
    roles: Optional[list]
    film_ids: Optional[list]



