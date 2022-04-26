from services.base import ElasticService, RedisService, QueryServise
from models.base import QueryBase
import json
from functools import lru_cache
from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from db.elastic import get_elastic
from db.redis import get_redis


class FilmService(RedisService, ElasticService, QueryServise):
    index = 'movies'

    async def __get_sort(self, field: str):
        direction = 'desc'
        if '-' in field:
            direction = 'asc'
            field = field.replace('-', '')
        sort_params = {
            'imdb_rating': {'imdb_rating': {"numeric_type": "double", "order": direction}},
        }
        return sort_params.get(field)

    async def __get_many_films_from_elastic(self, query: QueryBase):

        es_query = dict()
        es_query['size'] = 10000

        if query.sort:
            es_query['sort'] = [await self.__get_sort(query.sort)]

        if query.filter:
            index = query.filter.key
            _id = query.filter.values
            join_data = await self.get_by_id_from_elastic(
                index, _id
            )

            if not join_data:
                return None

            es_query['query'] = {
                "bool": {"must": [
                    {"match": {index: join_data.get('name')}},
                ]}
            }

        many_films = await self.get_from_elastic_by_query(self.index, es_query)
        return many_films

    async def __get_search_films_from_elastic(self, query: QueryBase):
        es_query = dict()
        es_query['size'] = 10000
        if query.query:
            es_query['query'] = {'multi_match': {
                'query': query.query,
                'fields': '*'
            }}
        many_films = await self.get_from_elastic_by_query(self.index, es_query)
        return many_films

    async def search_films_by_query(self, request):
        full_query = self.get_full_query(request.url)
        key = f'{self.index}_search_{str(full_query.__hash__())}'
        data = await self.get_many_from_redis(key)
        if not data:
            data = await self.__get_search_films_from_elastic(full_query)
            if not data:
                return None
            await self.put_data_redis(key, json.dumps(data))
        return data

    async def get_many_films_by_query(self, request):
        full_query = self.get_full_query(request.url)
        key = f'{self.index}_{full_query.__hash__()}'
        data = await self.get_many_from_redis(key)
        if not data:
            data = await self.__get_many_films_from_elastic(full_query)
            if not data:
                return None
            await self.put_data_redis(key, json.dumps(data))
        return data

    async def get_film(self, film_id: str):
        data = await self.get_one_from_redis(film_id)
        if not data:
            data = await self.get_by_id_from_elastic(self.index, film_id)
            if not data:
                return None
            await self.put_data_redis(film_id, json.dumps(data))
        return data


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> FilmService:
    return FilmService(redis, elastic)
