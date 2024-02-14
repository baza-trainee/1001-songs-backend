from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound

from src.database.database import get_async_session
from src.exceptions import SERVER_ERROR, NO_DATA_FOUND
from .models import Song


song_router = APIRouter(prefix="/song", tags=["Song"])


@song_router.get("")
async def get_song(session: AsyncSession = Depends(get_async_session)):
    try:
        records = await session.execute(select(Song))
        result = records.scalars().all()
        if not result:
            raise NoResultFound
        return result
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_DATA_FOUND)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SERVER_ERROR
        )
