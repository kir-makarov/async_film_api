import aioredis
import uvicorn as uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination
from db import elastic
from db import redis
import logging
from core.logger import LOGGING
from core.config import settings
from routers.base import api

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/docs',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    elastic.es = AsyncElasticsearch(hosts=[f'{settings.elastic.host}:{settings.elastic.port}'])
    redis.redis = aioredis.from_url(f"redis://{settings.redis.host}:{settings.redis.port}")


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


app.include_router(api, prefix="/api")
add_pagination(app)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True
    )
