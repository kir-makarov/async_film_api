import json
from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from services.film import FilmService, get_film_service
from models.film import FullFilm, ShortFilm
from fastapi_pagination import Page, paginate
from typing import Optional
from uuid import UUID
from core.config import error



router = APIRouter()


@router.get('/search', response_model=Page[ShortFilm])
async def search_films(
        request: Request,
        film_service: FilmService = Depends(get_film_service),
) -> paginate:
    try:
        films = await film_service.get_many_films_by_query(request)
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


@router.get('/', response_model=Page[ShortFilm])
async def many_films(
        request: Request,
        sort: Optional[str] = Query(None, regex="-imdb_rating|imdb_rating"),
        filter: Optional[UUID] = Query(None, alias='filter[genre|person]'),
        film_service: FilmService = Depends(get_film_service),
) -> paginate:

    try:
        films = await film_service.get_many_films_by_query(request)
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


@router.get('/{film_id}', response_model=FullFilm)
async def film_details(
        film_id: str,
        film_service: FilmService = Depends(get_film_service)
) -> FullFilm:
    try:
        film = await film_service.get_film(film_id)
        if not film:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=error.not_film
            )
        return FullFilm(**film)
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=error.services_error
        )

