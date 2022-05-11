import http

import pytest

pytestmark = pytest.mark.asyncio


async def test_genre_by_id(setup, redis_client, make_get_request):
    response = await make_get_request('/genres/a886d0ec-c3f3-4b16-b973-dedcf5bfa395', {})

    assert response.status == http.HTTPStatus.OK
    assert response.body == {"id": "a886d0ec-c3f3-4b16-b973-dedcf5bfa395", "name": "Short", }


async def test_genre_by_id_not_found(setup, redis_client, make_get_request):
    response = await make_get_request('/genres/some-non-existent-id', {})

    assert response.status == http.HTTPStatus.NOT_FOUND


async def test_genre_full_list(setup, redis_client, make_get_request):
    response = await make_get_request("/genres", {})

    assert response.status == http.HTTPStatus.OK


async def test_genre_by_cache(setup, redis_client, make_get_request):
    begin_response = await redis_client.get('{"page": {"number": "1", "size": "10"}, "index": "genre"}')
    await make_get_request("/genres", {"page[number]": 1, "page[size]": 10})
    redis_response = await redis_client.get('{"page": {"number": "1", "size": "10"}, "index": "genre"}')

    assert not begin_response
    assert redis_response
