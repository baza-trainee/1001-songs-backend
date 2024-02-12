from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page
from fastapi_pagination.ext.async_sqlalchemy import paginate

from src.database.database import get_async_session
from src.location.exceptions import NO_REGION_FOUND
from .service import get_records
from .models import NewsCategory, News
from .schemas import NewsSchema, NewCategorySchema
from sqlalchemy.orm.exc import NoResultFound


news_router = APIRouter(prefix="/news", tags=["News"])


@news_router.get("/categories", response_model=List[NewCategorySchema])
async def get_categories(session: AsyncSession = Depends(get_async_session)):
    return await get_records(NewsCategory, session)


@news_router.get("/news", response_model=Page[NewsSchema])
async def get_news(
    id: List[int] = Query(
        None, description="Press the button to add a field for a new ID"
    ),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Use this endpoint to retrieve news. You can filter them by category by passing one or more **category ID**s.
    """
    try:
        if session.scalar(select(func.count()).select_from(News)) == 0:
            raise NoResultFound
        if id:
            query = select(News).filter(News.category_id.in_(id))
        else:
            query = select(News)
        return await paginate(session, query)

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=NO_REGION_FOUND,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        )
