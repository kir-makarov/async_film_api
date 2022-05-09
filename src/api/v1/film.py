from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Request
from services.film import FilmService, get_film_service
from models.film import FullFilm, ShortFilm
from fastapi_pagination import Page, paginate
from typing import Optional, List
from core.config import error
from utils.get_param import get_params

router = APIRouter()


@router.get('/', response_model=List[ShortFilm])
@router.get('/search', response_model=List[ShortFilm])
async def many_films(
        request: Request,
        film_service: FilmService = Depends(get_film_service),
) -> List[ShortFilm]:
    params = get_params(request)
    film_list = await film_service.get_by_query(params=params)
    if not film_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=error.not_film)
    return [
        ShortFilm(**film)
        for film in film_list
    ]


@router.get('/{film_id}', response_model=Optional[FullFilm])
async def film_details(
        film_id: str,
        film_service: FilmService = Depends(get_film_service)
) -> FullFilm:
    film = await film_service.get_by_id(film_id)

    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=error.not_film
        )
    return FullFilm(**film)
