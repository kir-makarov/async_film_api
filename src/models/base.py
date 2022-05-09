import orjson
from pydantic import BaseModel, validator
from typing import Optional


class Filter(BaseModel):
    field: Optional[str]
    value: Optional[str]


class Page(BaseModel):
    number: int = 1
    size: int = 50

class QueryBase(BaseModel):

    query: Optional[str]
    sort: Optional[str]
    filter: Optional[dict]
    page: Optional[Page] = Page()
    total: Optional[str] = 10000

    @validator('filter')
    def filter_validator(cls, data: dict):
        field, value = list(data.items())[0]
        return Filter(field=field, value=value)


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class ORJSONModel(BaseModel):

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps