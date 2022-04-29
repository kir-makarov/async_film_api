import orjson
from pydantic import BaseModel, validator
from typing import Optional

def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class ORJSONModel(BaseModel):

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps

class Filter(ORJSONModel):

    key: str
    values: str

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

class QueryBase(ORJSONModel):

    query: Optional[str]
    filter: Optional[Filter]
    sort: Optional[str]

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))