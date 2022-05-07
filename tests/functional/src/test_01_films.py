import pytest


@pytest.mark.asyncio
async def test_search_detailed(redis_client, es_client, make_get_request):
    # Заполнение данных для теста
    # await es_client.bulk(...)

    # Выполнение запроса
    response = await make_get_request('/films/search', {'search': 'Star Wars'})

    # Проверка результата
    assert response.status == 404