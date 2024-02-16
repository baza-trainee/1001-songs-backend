from typing import Any

from fastapi import Request
from sqladmin import ModelView
from wtforms import TextAreaField

from src.admin.commons.formatters import MediaFormatter
from src.admin.commons.utils import model_change_for_files
from src.our_team.models import OurTeam
from src.utils import delete_photo


class OurTeamAdmin(ModelView, model=OurTeam):
    is_async = True

    name_plural = "Команда"
    category = "Про проєкт"
    icon = "fa-solid fa-people-group"

    column_l = [
        OurTeam.full_name,
        OurTeam.photo,
        OurTeam.description,
    ]
    column_exclude_list = ["id"]

    column_labels = {
        OurTeam.description: "Опис",
        OurTeam.full_name: "Повне ім'я",
        OurTeam.photo: "Фото",
    }

    column_formatters = {
        OurTeam.photo: MediaFormatter(),
    }
    form_overrides = {
        "description": TextAreaField,
    }
    form_args = {
        "description": {
            "render_kw": {
                "class": "form-control",
                "rows": 5,
                "maxlength": OurTeam.description.type.length,
            },
        },
    }
    can_edit = True
    can_create = True
    can_delete = True
    can_export = False

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        fields = ["photo"]
        await model_change_for_files(data, model, is_created, request, fields)
        return await super().on_model_change(data, model, is_created, request)

    async def on_model_delete(self, model: Any, request: Request) -> None:
        fields = ["photo"]
        for field in fields:
            await delete_photo(getattr(model, field, None))
        return await super().on_model_delete(model, request)
