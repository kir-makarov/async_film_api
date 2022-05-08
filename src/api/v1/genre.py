from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from services.genre import GenreService, get_genre_service
from models.genre import Genre
from core.config import error
from utils.get_param import get_params


router = APIRouter()


@router.get('/{genre_id}', response_model=Genre)
async def genre_details(
    genre_id: str,
    genre_service: GenreService = Depends(get_genre_service)
) -> Genre:
    try:
        genre = await genre_service.get_by_id(genre_id)
        if not genre:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=error.not_genre
            )
        return genre
    except Exception as err:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=error.services_error
        )


@router.get('/', response_model=List[Genre])
async def genre(
    request: Request,
    genre_service: GenreService = Depends(get_genre_service)
) -> List[Genre]:
    params = get_params(request)
    genres = await genre_service.get_by_query(params)
    if not genres:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=error.not_genre
        )
    return genres
