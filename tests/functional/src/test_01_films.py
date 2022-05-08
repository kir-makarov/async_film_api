import pytest


@pytest.mark.asyncio
async def test_search_detailed(setup, redis_client, make_get_request):
    # Заполнение данных для теста
    # await es_client.bulk(...)

    # Выполнение запроса
    response = await make_get_request('/films', {'page': 1, 'size': 50})

    # Проверка результата
    assert response.status == 404