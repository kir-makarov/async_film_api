import asyncio

import aioredis


async def main():
    while True:
        pong = None
        redis = None

        try:
            redis =  aioredis.from_url("redis://redis:6379")
            pong = await redis.ping()
        except Exception:
            print("Redis is down")

        if pong and redis:
            print("Redis is up!")
            await redis.close()
            break

        await asyncio.sleep(1)


asyncio.run(main())
