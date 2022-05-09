import os
from pydantic import BaseSettings
from core import es_shcema


class Base(BaseSettings):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        arbitrary_types_allowed = True

class RedisSettings(Base):
    host: str = os.getenv('REDIS_HOST', '127.0.0.1')
    port: str = os.getenv('REDIS_PORT', 6379)
    TTL: int = 60 * 5

    class Config:
        env_prefix = 'redis_'

class ElasticSchema(Base):
    movies = es_shcema.movies
    person = es_shcema.person
    genre = es_shcema.genre


class ElasticSettings(Base):

    host: str = os.getenv('ELASTIC_HOST', 'http://127.0.0.1')
    port: int = os.getenv('ELASTIC_PORT', 9200)
    es_schema: ElasticSchema = ElasticSchema()

    class Config:
        env_prefix = 'elastic_'

class Settings(Base):

    PROJECT_NAME: str = os.getenv('PROJECT_NAME', 'movies')
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    redis: RedisSettings = RedisSettings()
    elastic: ElasticSettings = ElasticSettings()


class Erorr(BaseSettings):

    not_film = 'films not found'
    not_genre = 'genre not found'
    not_person = 'person not found'

    services_error = 'services_error'


settings = Settings()
error = Erorr()