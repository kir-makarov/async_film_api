import asyncio
from elasticsearch import AsyncElasticsearch


async def main():
    while True:
        es = AsyncElasticsearch(hosts=["http://127.0.0.1:9200"])
        pong = await es.ping()
        if pong:
            print("ES is up!")
            await es.close()
            break
        print("Waiting for ES")
        await asyncio.sleep(1)


asyncio.run(main())
