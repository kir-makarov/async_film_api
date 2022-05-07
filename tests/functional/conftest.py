import asyncio
import json
from http import HTTPStatus

import aiohttp
import pytest
import aioredis

from typing import Optional
from dataclasses import dataclass

import pytest_asyncio
from elasticsearch._async.helpers import async_bulk
from multidict import CIMultiDictProxy
from elasticsearch import AsyncElasticsearch

SERVICE_URL = 'http://127.0.0.1:8000'


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest_asyncio.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts='https://127.0.0.1:9200')
    yield client
    await client.close()

@pytest.fixture(scope="session")
def predefined_data_generator():
    def inner():
        for filename in (
            "testdata/movies.json",
            "testdata/persons.json",
            "testdata/genres.json",
        ):
            yield json.load(open(filename))

    return inner


@pytest.fixture(scope="session")
def indices_data_generator():
    def inner():
        for index_name, filename in (
            ("movies", "testdata/index_films.json"),
            ("persons", "testdata/index_person.json"),
            ("genres", "testdata/index_genre.json"),
        ):
            yield index_name, json.load(open(filename))

    return inner

@pytest_asyncio.fixture(scope="session")
async def create_indices(indices_data_generator, es_client):
    indices_names = []
    for index_name, schema in indices_data_generator():
        indices_names.append(index_name)
        index_exists = await es_client.indices.exists(index=index_name)
        if not index_exists:
            await es_client.options(
                ignore_status=HTTPStatus.BAD_REQUEST
            ).indices.create(
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
        if response["hits"]["hits"]:
            break
        else:
            await asyncio.sleep(0.3)
            continue


@pytest_asyncio.fixture
async def setup(es_client, redis_client, fill_index):
    pass

@pytest.fixture(scope='function')
async def redis_client():
    redis = await aioredis.create_redis_pool(('127.0.0.1', 6379), minsize=10, maxsize=20)
    yield redis


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(session):
    async def inner(method: str, params: Optional[dict] = None) -> HTTPResponse:
        params = params or {}
        url = SERVICE_URL + '/api/v1' + method  # в боевых системах старайтесь так не делать!
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner
