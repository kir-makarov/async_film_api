import pytest


@pytest.mark.asyncio
async def test_genre_by_id(setup, redis_client, make_get_request):
    # request
    response = await make_get_request('/genres/a886d0ec-c3f3-4b16-b973-dedcf5bfa395', {})

    # assertion
    assert response.status == 200
    assert response.body == {"id": "a886d0ec-c3f3-4b16-b973-dedcf5bfa395", "name": "Short", }


@pytest.mark.asyncio
async def test_genre_full_list(setup, redis_client, make_get_request):
    response = await make_get_request("/genres", {})

    assert response.status == 200

@pytest.mark.asyncio
async def test_genre_by_cache(setup, redis_client, make_get_request):
    begin_response = await redis_client.get('{"page": {"number": "1", "size": "10"}, "index": "genre"}')
    await make_get_request("/genres", {"page[number]": 1, "page[size]": 10})
    redis_response = await redis_client.get('{"page": {"number": "1", "size": "10"}, "index": "genre"}')

    assert not begin_response
    assert redis_response


