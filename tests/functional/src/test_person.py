import pytest


@pytest.mark.asyncio
async def test_persons_simple(setup, redis_client, make_get_request):

    # request
    response = await make_get_request('/persons', {'page[number]': 1, 'page[size]': 20})

    # assertion
    assert response.status == 200