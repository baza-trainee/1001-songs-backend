from typing import Any

from fastapi import Request
from sqladmin import ModelView
from src.admin.commons.formatters import MediaFormatter

from src.admin.commons.utils import model_change_for_files
from src.payment.models import PaymentDetails
from src.utils import delete_photo


class PaymentAdmin(ModelView, model=PaymentDetails):
    is_async = True
    name_plural = "Реквізити"
    icon = "fa-solid fa-hand-holding-dollar"

    column_details_exclude_list = ["id"]
    column_exclude_list = ["id"]

    column_labels = {
        PaymentDetails.organization_name: "Назва організації",
        PaymentDetails.info: "Призначення платежу",
        PaymentDetails.qr_code_url: "QR code",
        PaymentDetails.coffee_url: "Coffee",
        PaymentDetails.iban: "IBAN",
    }
    can_export = False
    can_edit = True
    can_create = False
    can_delete = False

    column_formatters = {
        PaymentDetails.qr_code_url: MediaFormatter(),
    }

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        fields = ["qr_code_url"]
        await model_change_for_files(data, model, is_created, fields)
        return await super().on_model_change(data, model, is_created, request)

    async def on_model_delete(self, model: Any, request: Request) -> None:
        field = "qr_code_url"
        await delete_photo(getattr(model, field, None))
        return await super().on_model_delete(model, request)
