import pytest


@pytest.mark.asyncio
async def test_films_page_size_20(setup, redis_client, make_get_request):
    """ Tests that page_size==20 returns exactly 20 movies. """

    # request
    response = await make_get_request("/films", {"page[number]": 1, "page[size]": 20})

    # assertion
    assert response.status == 200
    assert len(response.body) == 20


@pytest.mark.asyncio
async def test_films_last_page(setup, redis_client, make_get_request):
    """ Tests that last page number is working correctly. """

    # request
    response = await make_get_request("/films", {"page[number]": 3, "page[size]": 10})

    # assertion
    assert response.status == 200
    assert len(response.body) == 6


@pytest.mark.asyncio
async def test_films_page_size_10(setup, redis_client, make_get_request):
    """ Tests to show only 10 films. """

    # request
    response = await make_get_request("/films", {"page[number]": 1, "page[size]": 10})

    # assertion
    assert response.status == 200
    assert len(response.body) == 10


@pytest.mark.asyncio
async def test_films_very_big_page_number(setup, redis_client, make_get_request):
    """ Test for very big page number (with no films on it). """

    # request
    response = await make_get_request("/films", {"page[number]": 5, "page[size]": 50})

    # assertion
    assert response.status == 404


@pytest.mark.asyncio
async def test_films_show_all_films(setup, redis_client, make_get_request):
    """ Test for showing all movies in index (ie limiting by big value). """

    # request
    response = await make_get_request("/films", {"page[number]": 1, "page[size]": 5000})

    # assertion
    assert response.status == 200
    assert len(response.body) == 26  # because we have 26 films in movies.json


@pytest.mark.asyncio
async def test_films_exact_film_by_id(setup, redis_client, make_get_request):
    """ Tests of exact film extraction by it's ID. """

    # request
    response = await make_get_request("/films/97f168bd-d10d-481b-ad38-89d252a13feb", {})

    # assertion
    assert response.status == 200
    assert response.body == {'id': '97f168bd-d10d-481b-ad38-89d252a13feb', 'imdb_rating': 7.8,
                             'genre': [{'id': '120a21cf-9097-479e-904a-13dd7198c1dd', 'name': 'Adventure'},
                                       {'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff', 'name': 'Action'},
                                       {'id': 'b92ef010-5e4c-4fd0-99d6-41b6456272cd', 'name': 'Fantasy'}],
                             'title': 'Star Wars Galaxies: Jump to Lightspeed',
                             'description': 'Set in the Star Wars timeframe between Episode IV and Episode V, Jump to Lightspeed is the first expansion for the Massively Multiplayer Online Role-Playing game set in the Star Wars ...',
                             'director': [], 'actors_names': None,
                             'writers_names': None}


@pytest.mark.asyncio
async def test_films_exact_film_by_id(setup, redis_client, make_get_request):
    """ Tests of exact film extraction by it's ID. """

    # requests
    redis_response_before_request = await redis_client.get("97f168bd-d10d-481b-ad38-89d252a13feb")
    await make_get_request("/films/97f168bd-d10d-481b-ad38-89d252a13feb", {})
    redis_response = await redis_client.get("97f168bd-d10d-481b-ad38-89d252a13feb")

    # assertion
    assert not redis_response_before_request  # nothing is in cache before request
    assert redis_response
    assert redis_response == b'{"id": "97f168bd-d10d-481b-ad38-89d252a13feb", "imdb_rating": 7.8, "genre": [{"id": "120a21cf-9097-479e-904a-13dd7198c1dd", "name": "Adventure"}, {"id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff", "name": "Action"}, {"id": "b92ef010-5e4c-4fd0-99d6-41b6456272cd", "name": "Fantasy"}], "title": "Star Wars Galaxies: Jump to Lightspeed", "description": "Set in the Star Wars timeframe between Episode IV and Episode V, Jump to Lightspeed is the first expansion for the Massively Multiplayer Online Role-Playing game set in the Star Wars ...", "director": [], "actors": null, "actors_names": null, "writers": null, "writers_names": null}'


@pytest.mark.asyncio
async def test_films_redis_page_size_10(setup, redis_client, make_get_request):
    """ Tests redis cache for 10 films request """

    # request
    redis_response_before_request = await redis_client.get('{"page": {"number": "1", "size": "10"}, "index": "movies"}')
    await make_get_request("/films", {"page[number]": 1, "page[size]": 10})
    redis_response = await redis_client.get('{"page": {"number": "1", "size": "10"}, "index": "movies"}')

    # assertion
    assert not redis_response_before_request  # nothing is in cache before request
    assert redis_response
    assert len(redis_response) == 4546   # we do not test exact value because it is ~5k in length
