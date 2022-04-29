from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from services.genre import GenreService, get_genre_service
from models.genre import Genre
from core.config import error

router = APIRouter()


@router.get('/{genre_id}', response_model=Genre)
async def genre_details(
    genre_id: str,
    genre_service: GenreService = Depends(get_genre_service)
) -> Genre:
    try:
        genre = await genre_service.get_genre(genre_id)
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
    genre_service: GenreService = Depends(get_genre_service)
) -> List[Genre]:
    try:
        genres = await genre_service.get_many_genres()
        if not genres:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=error.not_genre
            )
        return genres
    except Exception as err:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=error.services_error
        )