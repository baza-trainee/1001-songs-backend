from typing import Type, Optional

from fastapi import status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import ClauseElement
from src.exceptions import NO_DATA_FOUND, SERVER_ERROR
from src.database.database import Base
from .exceptions import NO_REGION_FOUND


async def get_records(model: Type[Base], session: AsyncSession):  # type: ignore
    try:
        records = await session.execute(select(model))
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


async def get_record(model: Type[Base], condition: Optional[ClauseElement], session: AsyncSession):  # type: ignore
    try:
        records = await session.execute(select(model).where(condition))
        result = records.scalars().all()
        if not result:
            raise NoResultFound
        return result
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=NO_REGION_FOUND % id,
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SERVER_ERROR
        )
