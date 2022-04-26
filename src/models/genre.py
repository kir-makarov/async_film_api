from models.base import ORJSONModel


class Genre(ORJSONModel):
    id: str
    name: str
