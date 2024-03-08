from typing import Any

from fastapi import Request

from src.admin.commons.base import BaseAdmin
from src.admin.commons.formatters import MediaFormatter
from src.admin.commons.utils import MediaInputWidget
from src.admin.commons.validators import MediaValidator
from src.config import MAX_IMAGE_SIZE_MB, IMAGE_TYPES
from src.database.redis import invalidate_cache
from src.payment.models import PaymentDetails


class PaymentAdmin(BaseAdmin, model=PaymentDetails):
    name_plural = "Реквізити"
    icon = "fa-solid fa-hand-holding-dollar"

    can_create = False
    can_delete = False

    column_labels = {
        PaymentDetails.organization_name: "Назва організації",
        PaymentDetails.bank: "Банк",
        PaymentDetails.edrpou: "ЄДРПОУ",
        PaymentDetails.iban: "IBAN",
        PaymentDetails.info: "Призначення платежу",
        PaymentDetails.qr_code_url: "QR code",
        PaymentDetails.patreon_url: "Patreon",
        PaymentDetails.coffee_url: "Coffee",
    }
    column_exclude_list = column_details_exclude_list = [
        PaymentDetails.id,
    ]

    column_formatters = {
        PaymentDetails.qr_code_url: MediaFormatter(),
    }
    form_files_list = [
        PaymentDetails.qr_code_url,
    ]
    form_args = {
        "qr_code_url": {
            "validators": [
                MediaValidator(
                    media_types=IMAGE_TYPES,
                    max_size=MAX_IMAGE_SIZE_MB,
                    is_required=True,
                )
            ],
            "widget": MediaInputWidget(is_required=True),
        },
    }

    async def after_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        await invalidate_cache("get_payment")
        return await super().after_model_change(data, model, is_created, request)
