from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from fastapi_pagination import Page
from fastapi_pagination.ext.async_sqlalchemy import paginate
from fastapi_cache.decorator import cache
from src.config import HOUR
from src.database.redis import my_key_builder
from src.database.database import get_async_session
from src.exceptions import NO_DATA_FOUND, SERVER_ERROR
from .models import OurProject
from .schemas import ProjectSchema, ProjectSliderSchema
from .exceptions import NO_PROJECT_FOUND


project_router = APIRouter(prefix="/projects", tags=["Projects"])


@project_router.get("", response_model=Page[ProjectSliderSchema])
@cache(expire=HOUR, key_builder=my_key_builder)
async def get_all_projects(
    project_exclude: Optional[int] = Query(None),
    session: AsyncSession = Depends(get_async_session),
):
    """By default, this endpoint returns data for the project slider.
    However, on the page of a specific project, this slider is also displayed.
    To prevent the currently viewed project from appearing in the slider,
    pass its **ID** to the optional field `project_exclude`,
    and you will get a slider with projects **excluding the current one**,
    on the page where the user is located."""
    try:
        query = select(OurProject)
        if project_exclude:
            query = query.filter(OurProject.id != project_exclude)
        query = query.order_by(OurProject.project_date.desc())
        result = await paginate(session, query)
        if not result.items:
            raise NoResultFound
        return result
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_DATA_FOUND)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@project_router.get("/{id}", response_model=ProjectSchema)
@cache(expire=HOUR, key_builder=my_key_builder)
async def get_project(id: int, session: AsyncSession = Depends(get_async_session)):
    """Returns data for the requested project page by **ID**."""
    try:
        record = await session.get(OurProject, id)
        if not record:
            raise NoResultFound
        return record
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=NO_PROJECT_FOUND % id
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
