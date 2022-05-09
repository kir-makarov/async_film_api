import asyncio
import json
from http import HTTPStatus

import aiohttp
import pytest
import aioredis

from typing import Optional
from dataclasses import dataclass

import pytest_asyncio
from multidict import CIMultiDictProxy
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

# SERVICE_URL = 'http://127.0.0.1:8000'
SERVICE_URL = 'http://api:8000'


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope='session')
async def es_client():
#    client = AsyncElasticsearch(hosts='http://127.0.0.1:9200')
    client = AsyncElasticsearch(hosts='http://es:9200')
    yield client
    await client.close()


@pytest.fixture(scope="session")
def predefined_data_generator():
    def inner():
        for filename in (
                # "../testdata/movies.json",
                # "../testdata/person.json",
                # "../testdata/genre.json",
                "/tests/testdata/movies.json",
                "/tests/testdata/person.json",
                "/tests/testdata/genre.json",
        ):
            yield json.load(open(filename))

    return inner


@pytest.fixture(scope="session")
def indices_data_generator():
    def inner():
        for index_name, filename in (
                # ("movies", "../testdata/index_films.json"),
                # ("person", "../testdata/index_person.json"),
                # ("genre", "../testdata/index_genre.json"),
                ("movies", "/tests/testdata/index_films.json"),
                ("person", "/tests/testdata/index_person.json"),
                ("genre", "/tests/testdata/index_genre.json"),
        ):
            yield index_name, json.load(open(filename))

    return inner


@pytest_asyncio.fixture(scope="session")
async def create_indices(indices_data_generator, es_client):
    indices_names = []
    for index_name, schema in indices_data_generator():
        indices_names.append(index_name)
        index_exists = await es_client.indices.exists(index=index_name)
        if index_exists:
            await es_client.indices.delete(index=index_name)
        await es_client.indices.create(
            index=index_name,
            mappings=schema["mappings"],
            settings=schema["settings"],
        )
    yield
    for index_name in indices_names:
        await es_client.indices.delete(index=index_name)


@pytest_asyncio.fixture(scope="session")
async def fill_index(es_client, create_indices, predefined_data_generator):
    for data in predefined_data_generator():
        await async_bulk(es_client, data)
    while True:
        response = await es_client.search(
            index="movies",
            query={"match_all": {}},
            size=20,
        )
        if response.get("hits", {}).get("hits", {}):
            break
        else:
            await asyncio.sleep(0.2)
            continue


@pytest_asyncio.fixture
async def setup(es_client, fill_index):
    pass


@pytest.fixture(scope='function')
async def redis_client():
#    redis = aioredis.from_url("redis://redis:6379")
    redis = aioredis.from_url("redis://127.0.0.1:6379")
    yield redis
    await redis.flushall()


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(session):
    async def inner(method: str, params: Optional[dict] = None) -> HTTPResponse:
        params = params or {}
        url = SERVICE_URL + '/api/v1' + method
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner
