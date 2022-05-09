from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Request
from services.person import PersonService, get_person_service
from models.person import FullPerson, ShortPerson
from fastapi_pagination import Page, paginate
from utils.get_param import get_params
from core.config import error
from typing import Optional


router = APIRouter()


@router.get('/', response_model=Page[ShortPerson])
@router.get('/search', response_model=Page[ShortPerson])
async def many_persons(
        request: Request,
        person_service: PersonService = Depends(get_person_service),
) -> paginate:
    params = get_params(request)
    person_list = await person_service.get_by_query(params)
    if not person_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=error.not_person)
    return paginate([
        ShortPerson(**person)
        for person in person_list
    ])


@router.get('/{person_id}', response_model=Optional[FullPerson])
async def person_details(
        person_id: str,
        person_service: PersonService = Depends(get_person_service),
) -> FullPerson:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=error.not_film
        )
    return FullPerson(**person)