import pytest


@pytest.mark.asyncio
async def test_films_page_size_20(setup, redis_client, make_get_request):
    """ Tests that page size 20 returns exactly 20 movies. """

    # request
    response = await make_get_request('/films', {'page[number]': 1, 'page[size]': 20})

    # assertion
    assert response.status == 200
    assert len(response.body) == 20


@pytest.mark.asyncio
async def test_films_last_page(setup, redis_client, make_get_request):
    """ Tests that last page number is working correctly """

    # request
    response = await make_get_request('/films', {'page[number]': 3, 'page[size]': 10})

    # assertion
    assert response.status == 200
    assert len(response.body) == 6


@pytest.mark.asyncio
async def test_films_page_size_10(setup, redis_client, make_get_request):
    """ Test for page size 10 """

    # request
    response = await make_get_request('/films', {'page[number]': 1, 'page[size]': 10})

    # assertion
    assert response.status == 200
    assert len(response.body) == 10


@pytest.mark.asyncio
async def test_films_very_big_page_number(setup, redis_client, make_get_request):
    """ Test for very big page number (with no films on it) """

    # request
    response = await make_get_request('/films', {'page[number]': 5, 'page[size]': 50})

    # assertion
    assert response.status == 404