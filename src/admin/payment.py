from typing import Any
from uuid import uuid4

from fastapi import Request
from sqladmin import ModelView
from src.admin.commons.utils import model_change_for_files

from src.payment.models import PaymentDetails
from src.utils import delete_photo


class PaymentAdmin(ModelView, model=PaymentDetails):
    is_async = True
    name_plural = "Реквізити"
    icon = "fa-solid fa-hand-holding-dollar"

    column_list = [
        PaymentDetails.info,
        PaymentDetails.iban,
        PaymentDetails.coffee_url,
        PaymentDetails.patreon_url,
        PaymentDetails.qr_code_url,
    ]
    column_details_exclude_list = ["id"]
    can_export = False
    can_edit = True
    can_create = False
    can_delete = False

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        fields = ["qr_code_url"]
        await model_change_for_files(data, model, is_created, fields)
        return await super().on_model_change(data, model, is_created, request)

    async def on_model_delete(self, model: Any, request: Request) -> None:
        await delete_photo(getattr(model, "qr_code_url", None))
        return await super().on_model_delete(model, request)
