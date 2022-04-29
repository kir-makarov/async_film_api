import json
from aioredis import Redis
from elasticsearch import AsyncElasticsearch
import re
from models.base import QueryBase, Filter
from urllib import parse
from core.config import settings


class Service:

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

class ElasticService(Service):

    async def get_by_id_from_elastic(self, index: str, _id: str):
        try:
            doc = await self.elastic.get(index, _id)
        except Exception as err:
            return None
        return doc['_source']

    async def get_from_elastic_by_query(self, index: str, es_query: dict):
        try:
            result = await self.elastic.search(
                index=index,
                body=es_query,
            )
            data = [
                doc['_source']
                for doc in result['hits']['hits']
            ]
        except Exception as err:
            return None
        return data


class RedisService(Service):

    async def put_data_redis(self, key, data):
        await self.redis.set(key, data, ex=settings.FILM_CACHE_EXPIRE_IN_SECONDS)

    async def get_one_from_redis(self, key):
        data = await self.redis.get(key)
        if not data:
            return None
        return json.loads(data.decode("utf-8"))

    async def get_many_from_redis(self, key):
        data = await self.redis.get(key)
        if not data:
            return None
        return json.loads(data.decode("utf-8"))

    async def get_hash(self, index, query):
        return


class QueryServise:

    def parse_filter(self, k):
        pars_filter = re.search(r'\[([^]]*)\]', k)
        if pars_filter:
            return pars_filter.group(1)
        raise AttributeError('filter error')


    def get_full_query(self, url):
        try:
            q = parse.parse_qs(url.query)
            good_dict = {}
            for k, v in q.items():
                if 'filter' in k:
                    good_dict['filter'] = Filter(
                        key=self.parse_filter(k),
                        values=v[0]
                    ).dict()
                good_dict[k] = v[0]
            return QueryBase(**good_dict)
        except Exception as err:
            return None