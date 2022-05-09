from aioredis import Redis
import aioredis.exceptions
from models.base import QueryBase
from elasticsearch import AsyncElasticsearch
import backoff
from elasticsearch.exceptions import ConnectionError, NotFoundError
from core.config import settings
import json
from typing import Union


class BaseService:

    def __init__(self, elastic: AsyncElasticsearch, redis: Redis):
        self.elastic = elastic
        self.redis = redis


class ElasticQueryMaker:

    def get_nested_filter(self, query):
        nested = dict()
        field = query.filter.field
        value = query.filter.value
        nested["nested"] = {
            "path": field,
            "query": {
                "bool": {"must": [
                    {"match": {field + ".id": value}},
                ]}
            }
        }
        return nested

    def get_search_query(self, query) -> dict:
        return {"multi_match": {"query": query.query}}

    def get_sort(self, query) -> dict:
        field = query.sort
        direction = 'desc'
        if '-' in field:
            direction = 'asc'
            field = field.replace('-', '')
        return {field: {'order': direction}}

    def es_body(self, params):
        query = QueryBase(**params)
        body = dict()
        if query.query:
            body.setdefault('query', {}).update(self.get_search_query(query))
        if query.filter:
            body.setdefault('query', {}).update(self.get_nested_filter(query))
        if query.sort:
            body['sort'] = self.get_sort(query)
        if query.page:
            body['from'] = (query.page.number - 1) * query.page.size
            body['size'] = query.page.size
        return body

    def key_body(self, index: str, key: Union[dict, str]):
        redis_key = dict()
        if type(key) == str:
            redis_key['index'] = index
            redis_key['key'] = key
            return json.dumps(redis_key)
        key['index'] = index
        return json.dumps(key)


class ElasticService(BaseService, ElasticQueryMaker):

    @backoff.on_exception(backoff.expo, ConnectionError, max_time=10)
    async def get_by_id_from_elastic(self, index: str, _id: str):
        try:
            doc = await self.elastic.get(index=index, id=_id)
            return doc['_source']
        except NotFoundError:
            return None

    @backoff.on_exception(backoff.expo, ConnectionError, max_time=10)
    async def get_by_query_from_elastic(self, index: str, body: dict):
        try:
            result = await self.elastic.search(index=index, body=body)
            data = [
                doc['_source']
                for doc in result['hits']['hits']
            ]
            return data
        except NotFoundError:
            return None


class RedisService(BaseService):

    @backoff.on_exception(backoff.expo, aioredis.exceptions.RedisError, max_time=10)
    async def put_data_redis(self, key: str, data: Union[dict, list]):
        await self.redis.set(key, json.dumps(data), ex=settings.redis.TTL)

    @backoff.on_exception(backoff.expo, aioredis.exceptions.RedisError, max_time=10)
    async def get_from_redis(self, key):
        data = await self.redis.get(key)
        if not data:
            return None
        return json.loads(data.decode("utf-8"))


class CacheService(RedisService, ElasticService):

    async def get_by_query(self, params: dict):
        key = self.key_body(self.index, params)
        data = await self.get_from_redis(key)
        if not data:
            body = self.es_body(params)
            data = await self.get_by_query_from_elastic(index=self.index, body=body)
            if not data:
                return None
            await self.put_data_redis(key, data)
        return data

    async def get_by_id(self, _id):
        data = await self.get_from_redis(_id)
        if not data:
            data = await self.get_by_id_from_elastic(index=self.index, _id=_id)
            if not data:
                return None
            await self.put_data_redis(_id, data)
        return data

    class Meta:
        def __init__(self, object):
            self.object = object
            getattr(self.object, "index")
