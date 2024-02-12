from typing import Any
from sqladmin import ModelView
from starlette.requests import Request
from wtforms import Form

from src.about.models import About
from src.admin.commons.formatters import format_quill
from src.admin.commons.utils import model_change_for_editor


class AboutAdmin(ModelView, model=About):
    is_async = True
    name_plural = "Про нас"
    icon = "fa-regular fa-address-card"

    column_list = [
        "title",
        "content",
    ]

    column_labels = {
        "title": "Заголовок",
        "content": "Контент",
    }

    can_view_details = False
    can_create = False
    can_delete = False
    can_export = False
    page_size_options = [1]
    page_size = 1
    column_formatters = {About.content: format_quill}

    async def scaffold_form(self) -> type[Form]:
        form = await super().scaffold_form()
        form.is_editor_field = [
            "content",
        ]
        del form.content.kwargs["validators"][-1]
        return form

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        await model_change_for_editor(data, model)
        return await super().on_model_change(data, model, is_created, request)
