import base64
import re
from typing import Any
from markupsafe import Markup
from sqladmin import ModelView
from starlette.requests import Request
from wtforms import Form

from src.about.models import About
from src.config import settings
from src.utils import delete_photo, model_change_for_editor, save_photo


class AboutAdmin(ModelView, model=About):
    name_plural = "Про нас"
    icon = "fa-regular fa-address-card"

    column_list = [
        "content",
    ]
    column_labels = {
        "content": "Контент",
    }
    can_view_details = False
    can_create = False
    can_delete = False
    can_export = False
    page_size_options = [1]
    page_size = 1
    column_formatters = {
        About.content: lambda m, a: Markup(
            f"<div class='markup-text'>{m.content}</div>"
        )
    }

    form_args = {
        "content": {
            "render_kw": {"class": "form-control", "rows": 10},
        },
    }

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
        model_change_for_editor(data, model, field_name="content")
        return await super().on_model_change(data, model, is_created, request)
