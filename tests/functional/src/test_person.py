import pytest


@pytest.mark.asyncio
async def test_persons_simple(setup, redis_client, make_get_request):

    # request
    response = await make_get_request('/persons', {'page': 1, 'size': 50})

    # assertion
    assert response.status == 200