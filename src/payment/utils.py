from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import AFTER_PAYMENT_CREATE
from .models import PaymentDetails


async def create_payment(payment_data: dict, session: AsyncSession):
    from src.utils import write_filetype_field

    try:
        payment_data["qr_code_url"] = await write_filetype_field(
            payment_data["qr_code_url"]
        )
        instance = PaymentDetails(**payment_data)
        session.add(instance)
        print(AFTER_PAYMENT_CREATE)
    except Exception as exc:
        raise exc
