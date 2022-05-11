import http

import pytest

pytestmark = pytest.mark.asyncio


async def test_films_page_size_20(setup, redis_client, make_get_request):
    """ Tests that page_size==20 returns exactly 20 movies. """

    response = await make_get_request("/films", {"page[number]": 1, "page[size]": 20})

    assert response.status == http.HTTPStatus.OK
    assert len(response.body) == 20


async def test_films_last_page(setup, redis_client, make_get_request):
    """ Tests that last page number is working correctly. """

    response = await make_get_request("/films", {"page[number]": 3, "page[size]": 10})

    assert response.status == http.HTTPStatus.OK
    assert len(response.body) == 6


async def test_films_page_size_10(setup, redis_client, make_get_request):
    """ Tests to show only 10 films. """

    response = await make_get_request("/films", {"page[number]": 1, "page[size]": 10})

    assert response.status == http.HTTPStatus.OK
    assert len(response.body) == 10


async def test_films_very_big_page_number(setup, redis_client, make_get_request):
    """ Test for very big page number (with no films on it). """

    response = await make_get_request("/films", {"page[number]": 5, "page[size]": 50})

    assert response.status == http.HTTPStatus.NOT_FOUND


async def test_films_show_all_films(setup, redis_client, make_get_request):
    """ Test for showing all movies in index (ie limiting by big value). """

    response = await make_get_request("/films", {"page[number]": 1, "page[size]": 5000})

    assert response.status == http.HTTPStatus.OK
    assert len(response.body) == 26  # because we have 26 films in movies.json


async def test_films_exact_film_by_id(setup, redis_client, make_get_request):
    """ Tests exact film extraction by it's ID. """

    response = await make_get_request("/films/97f168bd-d10d-481b-ad38-89d252a13feb", {})

    assert response.status == http.HTTPStatus.OK
    assert response.body == {'id': '97f168bd-d10d-481b-ad38-89d252a13feb', 'imdb_rating': 7.8,
                             'genre': [{'id': '120a21cf-9097-479e-904a-13dd7198c1dd', 'name': 'Adventure'},
                                       {'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff', 'name': 'Action'},
                                       {'id': 'b92ef010-5e4c-4fd0-99d6-41b6456272cd', 'name': 'Fantasy'}],
                             'title': 'Star Wars Galaxies: Jump to Lightspeed',
                             'description': 'Set in the Star Wars timeframe between Episode IV and Episode V, Jump to Lightspeed is the first expansion for the Massively Multiplayer Online Role-Playing game set in the Star Wars ...',
                             'director': [], 'actors_names': None,
                             'writers_names': None}


async def test_films_exact_film_by_id(setup, redis_client, make_get_request):
    """ Tests exact film extraction by it's ID. """

    redis_response_before_request = await redis_client.get("97f168bd-d10d-481b-ad38-89d252a13feb")
    await make_get_request("/films/97f168bd-d10d-481b-ad38-89d252a13feb", {})
    redis_response_after_request = await redis_client.get("97f168bd-d10d-481b-ad38-89d252a13feb")

    assert not redis_response_before_request  # nothing is in the cache before request
    assert redis_response_after_request
    assert redis_response_after_request == b'{"id": "97f168bd-d10d-481b-ad38-89d252a13feb", "imdb_rating": 7.8, "genre": [{"id": "120a21cf-9097-479e-904a-13dd7198c1dd", "name": "Adventure"}, {"id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff", "name": "Action"}, {"id": "b92ef010-5e4c-4fd0-99d6-41b6456272cd", "name": "Fantasy"}], "title": "Star Wars Galaxies: Jump to Lightspeed", "description": "Set in the Star Wars timeframe between Episode IV and Episode V, Jump to Lightspeed is the first expansion for the Massively Multiplayer Online Role-Playing game set in the Star Wars ...", "director": [], "actors": null, "actors_names": null, "writers": null, "writers_names": null}'


async def test_films_redis_page_size_10(setup, redis_client, make_get_request):
    """ Tests redis cache for 10 films request """

    redis_response_before_request = await redis_client.get('{"page": {"number": "1", "size": "10"}, "index": "movies"}')
    await make_get_request("/films", {"page[number]": 1, "page[size]": 10})
    redis_response_after_request = await redis_client.get('{"page": {"number": "1", "size": "10"}, "index": "movies"}')

    assert not redis_response_before_request  # nothing is in cache before request
    assert redis_response_after_request
    assert len(redis_response_after_request) == 4546  # we do not test exact value because it is ~5k in length


async def test_films_search_by_part_of_name(setup, redis_client, make_get_request):
    """ Tests search by part of the film name """

    # request
    response = await make_get_request("/films", {"query": "Wookiees"})

    # assertion
    assert response.status == http.HTTPStatus.OK
    assert response.body == [{'id': 'bf3bd131-b844-4585-9974-6c374cff2371', 'imdb_rating': 6.9,
                              'genre': [{'id': '120a21cf-9097-479e-904a-13dd7198c1dd', 'name': 'Adventure'},
                                        {'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff', 'name': 'Action'},
                                        {'id': 'b92ef010-5e4c-4fd0-99d6-41b6456272cd', 'name': 'Fantasy'}],
                              'title': 'Star Wars Galaxies: Rage of the Wookiees'}]


async def test_films_search_not_existent_name(setup, redis_client, make_get_request):
    """ Tests search for film which not exist in the index """

    response = await make_get_request("/films", {"query": "asdfasdfasdf"})

    assert response.status == http.HTTPStatus.NOT_FOUND
    assert response.body == {'detail': 'films not found'}


async def test_films_search_redis_cashe(setup, redis_client, make_get_request):
    """ Tests redis cache hit of search query  """

    redis_response_before_request = await redis_client.get('{"query": "Star", "index": "movies"}')
    response = await make_get_request("/films", {"query": "Star"})
    redis_response_after_request = await redis_client.get('{"query": "Star", "index": "movies"}')

    assert not redis_response_before_request
    assert response.status == http.HTTPStatus.OK
    assert len(response.body) == 26  # all our films have `star` word in their names
    assert redis_response_after_request
    assert len(redis_response_after_request) == 20789


async def test_films_sort_imdb_rating(setup, redis_client, make_get_request):
    """ Tests ascending and descending sort order for imdb_rating  """

    response_descending = await make_get_request("/films", {"sort": "-imdb_rating"})
    response_ascending = await make_get_request("/films", {"sort": "imdb_rating"})

    assert response_ascending.status == http.HTTPStatus.OK
    assert response_descending.status == http.HTTPStatus.OK

    assert response_descending.body[0] == response_ascending.body[-1]
