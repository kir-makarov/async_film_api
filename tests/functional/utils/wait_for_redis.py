import asyncio

import aioredis


async def main():
    while True:
        pong = None
        redis = None

        try:
            redis = await aioredis.create_redis_pool(('127.0.0.1', 6379), minsize=10, maxsize=20)
            pong = await redis.ping()
        except Exception:
            print("Redis is down")

        if pong:
            print("Redis is up!")
            redis.close()
            break

        await asyncio.sleep(1)


asyncio.run(main())
