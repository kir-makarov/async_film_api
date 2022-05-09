from elasticsearch import AsyncElasticsearch
import backoff
from elasticsearch import exceptions
from loguru import logger
from core.config import settings
import asyncio



@backoff.on_exception(backoff.expo, exceptions.ConnectionError, logger=logger)
async def create_index(es: AsyncElasticsearch, index: str, schema: dict) -> None:
    res = await es.indices.create(
        index=index,
        body=schema,
        ignore=400
    )
    if res.get('acknowledged'):
        logger.info(f'{index} index created')
    else:
        logger.warning(f'{index} {res.get("error").get("reason")}')


async def check_index(es) -> None:
    shemas = settings.elastic.es_schema.dict()
    for index, schema in shemas.items():
        await create_index(es, index, schema)


async def run():
    es = AsyncElasticsearch(hosts=[f'{settings.elastic.host}:{settings.elastic.port}'])
    await check_index(es)
    await es.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())

