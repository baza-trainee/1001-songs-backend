from typing import Any
from fastapi import Request
from src.about.models import About
from src.admin.commons.base import BaseAdmin
from src.admin.commons.formatters import format_quill
from src.database.redis import invalidate_cache


class AboutAdmin(BaseAdmin, model=About):
    name_plural = "Про нас"
    category = "Про проєкт"
    icon = "fa-regular fa-address-card"

    can_create = False
    can_delete = False

    column_labels = {
        About.title: "Заголовок",
        About.content: "Контент",
    }
    column_exclude_list = column_details_exclude_list = [
        About.id,
    ]
    column_formatters = {
        About.content: format_quill,
    }
    form_quill_list = [
        About.content,
    ]

    async def after_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        await invalidate_cache("get_about")
        return await super().after_model_change(data, model, is_created, request)

    async def after_model_delete(self, model: Any, request: Request) -> None:
        await invalidate_cache("get_about")
        return await super().after_model_delete(model, request)
