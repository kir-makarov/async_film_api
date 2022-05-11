import asyncio

import aioredis

WAIT_UNTIL_TIMEOUT = 15

async def main():
    attempt = 0

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

        attempt += 1
        if attempt >= WAIT_UNTIL_TIMEOUT:
            print("Redis timeout")
            break

        await asyncio.sleep(1)


asyncio.run(main())
