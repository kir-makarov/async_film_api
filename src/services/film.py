from functools import lru_cache
from fastapi import Depends
from db.elastic import get_elastic
from db.redis import get_redis
from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from services.base import CacheService


class FilmService(CacheService):
    index = 'movies'


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(elastic, redis)
