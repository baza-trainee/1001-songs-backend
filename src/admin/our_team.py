from typing import Any
from fastapi import Request
from wtforms import TextAreaField

from src.admin.commons.base import BaseAdmin
from src.admin.commons.exceptions import IMG_REQ
from src.admin.commons.formatters import MediaFormatter
from src.admin.commons.utils import MediaInputWidget
from src.admin.commons.validators import MediaValidator
from src.config import IMAGE_TYPES, MAX_IMAGE_SIZE_MB
from src.database.redis import invalidate_cache
from src.our_team.models import OurTeam

PHOTO_RES = (410, 560)


class OurTeamAdmin(BaseAdmin, model=OurTeam):
    name_plural = "Команда"
    category = "Про проєкт"
    icon = "fa-solid fa-people-group"

    column_exclude_list = column_details_exclude_list = [
        OurTeam.id,
    ]

    column_labels = {
        OurTeam.description: "Опис",
        OurTeam.full_name: "Повне ім'я",
        OurTeam.photo: "Фото",
    }
    column_formatters = {
        OurTeam.photo: MediaFormatter(),
    }
    form_files_list = [
        OurTeam.photo,
    ]
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
        "photo": {
            "widget": MediaInputWidget(is_required=True),
            "validators": [
                MediaValidator(
                    media_types=IMAGE_TYPES,
                    max_size=MAX_IMAGE_SIZE_MB,
                    is_required=True,
                ),
            ],
            "description": IMG_REQ % PHOTO_RES,
        },
    }

    async def after_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        await invalidate_cache("get_team_list")
        return await super().after_model_change(data, model, is_created, request)

    async def after_model_delete(self, model: Any, request: Request) -> None:
        await invalidate_cache("get_team_list")
        return await super().after_model_delete(model, request)
