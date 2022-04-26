from functools import lru_cache
from db.elastic import get_elastic
from db.redis import get_redis
from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from services.base import ElasticService, RedisService
import json


class GenreService(RedisService, ElasticService):

    index = 'genre'

    async def get_genre(self,  genre_id: str):
        data = await self.get_many_from_redis(genre_id)
        if not data:
            data = await self.get_by_id_from_elastic(self.index, genre_id)
            if not data:
                return None
            await self.put_data_redis(genre_id, json.dumps(data))
        return data

    async def get_many_genres_from_elastic(self):
        es_query = dict()
        es_query['size'] = 10000
        many_persons = await self.get_from_elastic_by_query(
            self.index, es_query
        )
        return many_persons

    async def get_many_genres(self):
        key = 'genres'
        data = await self.get_many_from_redis(key)
        if not data:
            data = await self.get_many_genres_from_elastic()
            if not data:
                return None
            await self.put_data_redis(key, json.dumps(data))
        return data


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> GenreService:
    return GenreService(redis, elastic)
