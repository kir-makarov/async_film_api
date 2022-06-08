import json
from functools import wraps
from http import HTTPStatus

import aiohttp
from aiohttp import ClientConnectionError
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi_pagination import Page, paginate
from typing import Optional, List

from core import const
from services.film import FilmService, get_film_service
from models.film import FullFilm, ShortFilm
from core.config import error, settings
from utils.get_param import get_params

router = APIRouter()


def authenticate_user(func):
    @wraps(func)
    async def wrapper(*args, request: Request, **kwargs):
        auth_header = request.headers.get("Authorization")
        headers = {"Authorization": auth_header}
        result_role = const.ACCESS_GUEST

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(settings.AUTH_VALIDATION_URL,
                                        headers=headers) as resp:
                    content = await resp.content.read()
                    content_json = json.loads(content.decode())
                    verified = content_json.get("verified")
                    if verified:
                        result_role = content_json.get("role", const.ACCESS_GUEST)
        except ClientConnectionError:  # in case of /auth service unavailable
            result_role = const.ACCESS_GUEST

        kwargs['role'] = result_role
        return await func(*args, request, **kwargs)

    return wrapper


@router.get('/', response_model=List[ShortFilm])
@router.get('/search', response_model=List[ShortFilm])
@authenticate_user
async def many_films(
        request: Request,
        film_service: FilmService = Depends(get_film_service),
        **kwargs) -> List[ShortFilm]:
    params = get_params(request)
    film_list = await film_service.get_by_query(params=params)

    role = kwargs["role"]
    if role == const.ACCESS_GUEST:
        film_list = [film for film in film_list if film.get("imdb_rating") and film.get("imdb_rating") <= 8]

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
