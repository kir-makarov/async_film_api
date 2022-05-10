import pytest


@pytest.mark.asyncio
async def test_persons_by_id(setup, redis_client, make_get_request):
    # request
    response = await make_get_request('/persons/3214cf58-8dbf-40ab-9185-77213933507e', {})

    # assertion
    assert response.status == 200
    assert response.body == {"id": "3214cf58-8dbf-40ab-9185-77213933507e", "full_name": "Richard Marquand",
                             "roles": ["director"], "film_ids": ["025c58cd-1b7e-43be-9ffb-8571a613579b"]}


@pytest.mark.asyncio
async def test_person_page_size_20(setup, redis_client, make_get_request):
    response = await make_get_request("/persons", {"page[number]": 1, "page[size]": 20})

    assert response.status == 200
    assert len(response.body) == 20


# @pytest.mark.asyncio
# async def test_person_films(setup, redis_client, make_get_request):
#     response = await make_get_request("/persons/3214cf58-8dbf-40ab-9185-77213933507e/film/", {})
#
#     assert response.status == 200


@pytest.mark.asyncio
async def test_all_person(setup, redis_client, make_get_request):
    response = await make_get_request("/persons", {})

    assert response.status == 200
    assert len(response.body) == 26


@pytest.mark.asyncio
async def test_person_by_id_cache(setup, redis_client, make_get_request):
    begin_response = await redis_client.get('{"page": {"number": "1", "size": "10"}, "index": "person"}')
    await make_get_request("/persons", {"page[number]": 1, "page[size]": 10})
    redis_response = await redis_client.get('{"page": {"number": "1", "size": "10"}, "index": "person"}')

    assert not begin_response
    assert redis_response


@pytest.mark.asyncio
async def test_person_search_name(setup, redis_client, make_get_request):
    response = await make_get_request("/persons", {"query": "Neeson"})

    # assertion
    assert response.status == 200
    assert response.body == [{"id": "39abe5bd-33b3-44e8-8c12-2e360e2fa621", "full_name": "Liam Neeson"}]
