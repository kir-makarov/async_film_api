from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from services.person import PersonService, get_person_service
from models.person import FullPerson, ShortPerson
from models.base import QueryBase
from fastapi_pagination import Page, paginate
from models.film import ShortFilm

router = APIRouter()


@router.get('/search', response_model=Page[ShortPerson])
async def search_persons(
        person_service: PersonService = Depends(get_person_service),
        query: QueryBase = Depends()
) -> paginate:
    persons = await person_service.search_persons_by_query(query)
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='persons not found'
        )
    return paginate([
        ShortPerson(**person)
        for person in persons
    ])


@router.get('/{person_id}', response_model=FullPerson)
async def person_details(
        person_id: str,
        person_service: PersonService = Depends(get_person_service)
) -> FullPerson:
    person = await person_service.get_person(person_id)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='person not found'
        )
    return FullPerson(**person)


@router.get('/{person_id}/film', response_model=Page[ShortFilm])
async def fims_by_person(
        person_id: str,
        person_service: PersonService = Depends(get_person_service)
):
    films = await person_service.get_films_by_person(person_id)
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='persons not found'
        )
    return paginate([
        ShortFilm(**film)
        for film in films
    ])


@router.get('/', response_model=Page[ShortPerson])
async def many_persons(
        person_service: PersonService = Depends(get_person_service),
) -> paginate:
    persons = await person_service.get_many_persons()
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='persons not found'
        )
    return paginate([
        ShortPerson(**person)
        for person in persons
    ])
