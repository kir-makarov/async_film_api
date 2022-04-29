from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from services.person import PersonService, get_person_service
from models.person import FullPerson, ShortPerson
from models.base import QueryBase
from fastapi_pagination import Page, paginate
from models.film import ShortFilm

from core.config import error

router = APIRouter()


@router.get('/search', response_model=Page[ShortPerson])
async def search_persons(
        person_service: PersonService = Depends(get_person_service),
        query: QueryBase = Depends()
) -> paginate:
    try:
        persons = await person_service.search_persons_by_query(query)
        if not persons:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=error.not_person
            )
        return paginate([
            ShortPerson(**person)
            for person in persons
        ])
    except Exception as err:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=error.services_error
        )


@router.get('/{person_id}', response_model=FullPerson)
async def person_details(
        person_id: str,
        person_service: PersonService = Depends(get_person_service)
) -> FullPerson:
    try:
        person = await person_service.get_person(person_id)
        if not person:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=error.not_person
            )
        return FullPerson(**person)
    except Exception as err:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=error.services_error
        )

@router.get('/{person_id}/film', response_model=Page[ShortFilm])
async def fims_by_person(
        person_id: str,
        person_service: PersonService = Depends(get_person_service)
):
    try:
        films = await person_service.get_films_by_person(person_id)
        if not films:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=error.not_film
            )
        return paginate([
            ShortFilm(**film)
            for film in films
        ])
    except Exception as err:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=error.services_error
        )


@router.get('/', response_model=Page[ShortPerson])
async def many_persons(
        person_service: PersonService = Depends(get_person_service),
) -> paginate:
    try:
        persons = await person_service.get_many_persons()
        if not persons:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=error.not_person
            )
        return paginate([
            ShortPerson(**person)
            for person in persons
        ])
    except Exception as err:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=error.services_error
        )
