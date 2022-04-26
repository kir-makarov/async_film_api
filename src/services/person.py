from functools import lru_cache
from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from services.base import ElasticService, RedisService
from db.elastic import get_elastic
from db.redis import get_redis
from models.base import QueryBase
import json


class PersonService(RedisService, ElasticService):

    index = 'person'

    async def __get_many_persons_from_elastic(self):
        es_query = dict()
        es_query['size'] = 10000
        many_persons = await self.get_from_elastic_by_query(
            self.index, es_query
        )
        return many_persons

    async def __get_search_person_from_elastic(self, query: QueryBase):
        es_query = dict()
        es_query['size'] = 10000
        if query.query:
            es_query['query'] = {
                "match": {"full_name": {"query": query.query, "fuzziness": "AUTO"}}
            }
        many_films = await self.get_from_elastic_by_query(self.index, es_query)
        return many_films

    async def get_films_by_person(self, person_id: str):
        h_query = 'films_by' + person_id
        data = await self.get_many_from_redis(h_query)
        if not data:
            person = await self.get_by_id_from_elastic(self.index, person_id)
            if not person.get('film_ids'):
                return None
            es_query = dict()
            es_query['query'] = {
                "ids": {"values": person.get('film_ids')}
            }
            data = await self.get_from_elastic_by_query('movies', es_query)
            if not data:
                return None
            await self.put_data_redis(h_query, json.dumps(data))
        return data

    async def get_many_persons(self):
        h_query = self.index
        data = await self.get_many_from_redis(h_query)
        if not data:
            data = await self.__get_many_persons_from_elastic()
            if not data:
                return None
            await self.put_data_redis(h_query, json.dumps(data))
        return data

    async def search_persons_by_query(self, query: QueryBase):
        h_query = f'search_{self.index}' + str(query.__hash__())
        data = await self.get_many_from_redis(h_query)
        if not data:
            data = await self.__get_search_person_from_elastic(query)
            if not data:
                return None
            await self.put_data_redis(h_query, json.dumps(data))
        return data

    async def get_person(self, person_id: str):
        data = await self.get_one_from_redis(person_id)
        if not data:
            data = await self.get_by_id_from_elastic(self.index, person_id)
            if not data:
                return None
            await self.put_data_redis(person_id, json.dumps(data))
        return data


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> PersonService:
    return PersonService(redis, elastic)
