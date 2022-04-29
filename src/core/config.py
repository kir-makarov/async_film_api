import os
from pydantic import BaseSettings



class RedisSettings(BaseSettings):
    HOST: str = os.getenv('REDIS_HOST', '127.0.0.1')
    PORT: int = os.getenv('REDIS_PORT', 6379)
    TTL: int = 60 * 5


class ElasticSettings(BaseSettings):
    HOST: str = os.getenv('ELASTIC_HOST', '127.0.0.1')
    PORT: int = os.getenv('ELASTIC_PORT', 9200)



class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv('PROJECT_NAME', 'movies')
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    REDIS: RedisSettings = RedisSettings()
    ELASTIC: ElasticSettings = ElasticSettings()

    FILM_CACHE_EXPIRE_IN_SECONDS: int = 60 * 5

    class Config:
        env_file = '.env'


class Erorr(BaseSettings):

    not_film = 'films not found'
    not_genre = 'genre not found'
    not_person = 'person not found'

    services_error = 'services_error'

settings = Settings()
error = Erorr()


