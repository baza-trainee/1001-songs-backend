from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from fastapi_cache.decorator import cache

from src.config import HOUR
from src.database.redis import my_key_builder
from src.database.database import get_async_session
from src.exceptions import NO_DATA_FOUND, SERVER_ERROR
from .schemas import PaymentDetailsSchema
from .models import PaymentDetails


payment_router = APIRouter(prefix="/payment", tags=["Payment"])


@payment_router.get("", response_model=PaymentDetailsSchema)
@cache(expire=HOUR, key_builder=my_key_builder)
async def get_payment(
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
