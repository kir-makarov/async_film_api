import pytest


@pytest.mark.asyncio
async def test_genres_simple(setup, redis_client, make_get_request):

    # request
    response = await make_get_request('/genres', {})

    # assertion
    assert response.status == 200