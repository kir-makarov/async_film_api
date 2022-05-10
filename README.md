# Async Api

###Get started

_____________________

1. Создаем директорию назовем её `kinozal`:
2. Используя `git` скачиваем все микросервисы задействованные в данном проекте:
    ```bash
    git clone git@gitlab.com:kinozal/admin-panel.git
    git clone https://github.com/kir-makarov/async_film_api.git
    git clone git@gitlab.com:kinozal/etl.git
    ```
    В директории `kinozal` находятся 3 микросервиса `admin-panel`, `async_film_api` и `etl`
3. Сервисы поднимаются в `docker` контейнерах находясь в корневой директории сервиса выполнить команду
   ```bash
   docker-compose up --build -d 
   ```

##Async Api
#### FastAPI, Elasticsearch, Redis, Nginx

В результате сборки проекта async_film_api разворачиваются следующие контейнеры:
 - elasticsearch
 - redis
 - nginx
 - api

Также при страте контейнера с api, скриптом `entrypoint.sh` созданются индексы. \
Настройки индексов хранятся в файле `es_schema.py` в папке `core`.

Для наполнения Elasticsearch начальными данными используется [**ETL**](clone git@gitlab.com:kinozal/etl.git)
ETL поднимается последним после сборки [**Admin Panel**](https://gitlab.com/kinozal/admin-panel) и [**Async API**](https://github.com/kir-makarov/async_film_api) 