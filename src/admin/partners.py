from typing import Any

from fastapi import Request
from wtforms import URLField

from src.admin.commons.base import BaseAdmin
from src.admin.commons.exceptions import IMG_REQ
from src.admin.commons.formatters import MediaFormatter
from src.admin.commons.utils import MediaInputWidget
from src.admin.commons.validators import MediaValidator, validate_url
from src.config import EXTENDED_IMAGE_TYPE, MAX_IMAGE_SIZE_MB
from src.database.redis import invalidate_cache
from src.partners.models import Partners

PHOTO_RES = (200, 200)


class PartnersAdmin(BaseAdmin, model=Partners):
    name_plural = "Партнери"
    category = "Про проєкт"
    icon = "fa-solid fa-handshake"

    column_exclude_list = [
        Partners.id,
    ]
    column_labels = {
        Partners.link: "Посилання",
        Partners.photo: "Фото",
    }
    form_overrides = {
        "link": URLField,
    }
    column_formatters = {
        Partners.photo: MediaFormatter(),
    }
    form_files_list = [
        Partners.photo,
    ]
    form_args = {
        "link": {
            "validators": [validate_url],
            "render_kw": {
                "class": "form-control",
                "maxlength": Partners.link.type.length,
            },
        },
        "photo": {
            "widget": MediaInputWidget(is_required=True),
            "validators": [
                MediaValidator(
                    media_types=EXTENDED_IMAGE_TYPE,
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
        await invalidate_cache("get_partners")
        return await super().after_model_change(data, model, is_created, request)

    async def after_model_delete(self, model: Any, request: Request) -> None:
        await invalidate_cache("get_partners")
        return await super().after_model_delete(model, request)
