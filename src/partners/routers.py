from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from fastapi_cache.decorator import cache

from src.config import HOUR
from src.database.redis import my_key_builder
from src.database.database import get_async_session
from src.exceptions import NO_DATA_FOUND, SERVER_ERROR
from .models import Partners
from .schemas import PartnersSchema


partners_router = APIRouter(prefix="/partners", tags=["Partners"])


@partners_router.get("", response_model=List[PartnersSchema])
@cache(expire=HOUR, key_builder=my_key_builder)
async def get_partners(
    session: AsyncSession = Depends(get_async_session),
):
    try:
        query = select(Partners).order_by("id")
        story = await session.execute(query)
        response = story.scalars().all()
        if not response:
            raise NoResultFound
        return response
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_DATA_FOUND)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SERVER_ERROR
        )
