from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound

from src.database.database import get_async_session
from src.exceptions import NO_DATA_FOUND, SERVER_ERROR
from .schemas import PaymentDetailsSchema
from .models import PaymentDetails


payment_router = APIRouter(prefix="/payment", tags=["Payment"])


@payment_router.get("", response_model=PaymentDetailsSchema)
async def get_hero(
    session: AsyncSession = Depends(get_async_session),
):
    try:
        record = await session.get(PaymentDetails, 1)
        if not record:
            raise NoResultFound
        return record
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_DATA_FOUND)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SERVER_ERROR
        )
