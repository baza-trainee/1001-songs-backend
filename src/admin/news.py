from typing import Any
from fastapi import Request
from wtforms.validators import DataRequired

from src.admin.commons.base import BaseAdmin
from src.admin.commons.exceptions import IMG_REQ
from src.admin.commons.formatters import (
    MediaFormatter,
    TextFormatter,
    format_date,
    format_quill,
    ArrayFormatter,
)
from src.admin.commons.utils import CustomSelect2TagsField, MediaInputWidget
from src.admin.commons.validators import (
    ArrayStringValidator,
    MediaValidator,
    PastDateValidator,
)
from src.config import IMAGE_TYPES, MAX_IMAGE_SIZE_MB
from src.database.redis import invalidate_cache, invalidate_cache_partial
from src.news.models import News
from src.our_team.models import OurTeam

PREVIEW_PHOTO_RES = (630, 320)
CONTENT_PHOTO_RES = (1780, 1090)
MODEL_TEAM_FIELDS = ["authors", "editors", "photographers"]


class NewsAdmin(BaseAdmin, model=News):
    name_plural = "Новини"
    icon = "fa-solid fa-kiwi-bird"
    save_as = True

    column_labels = {
        News.title: "Заголовок",
        News.content: "Контент",
        News.short_description: "Короткий опис",
        News.authors: "Автор",
        News.editors: "Редактор",
        News.photographers: "Світлини",
        News.preview_photo: "Фото прев'ю",
        News.location: "Розташування",
        News.category: "Категорія",
        News.created_at: "Дата",
    }

    column_list = [
        News.title,
        News.content,
        News.short_description,
        News.preview_photo,
        News.location,
        News.created_at,
        News.category,
        News.authors,
        News.editors,
        News.photographers,
    ]
    column_searchable_list = [
        News.title,
    ]
    column_sortable_list = [
        News.created_at,
    ]
    form_columns = [
        News.title,
        News.short_description,
        News.preview_photo,
        News.location,
        News.created_at,
        News.category,
        News.authors,
        News.editors,
        News.photographers,
        News.content,
    ]

    column_formatters = {
        News.title: TextFormatter(text_align="left"),
        News.created_at: format_date,
        News.content: format_quill,
        News.authors: ArrayFormatter(),
        News.editors: ArrayFormatter(),
        News.photographers: ArrayFormatter(),
        News.preview_photo: MediaFormatter(),
    }
    form_quill_list = [
        News.content,
    ]
    form_files_list = [
        News.preview_photo,
    ]
    form_overrides = {
        **{field: CustomSelect2TagsField for field in MODEL_TEAM_FIELDS},
    }
    form_args = {
        "created_at": {"validators": [PastDateValidator()]},
        "location": {"validators": [DataRequired()]},
        "category": {"validators": [DataRequired()]},
        **{
            field: {"model": OurTeam, "validators": [ArrayStringValidator()]}
            for field in MODEL_TEAM_FIELDS
        },
        "preview_photo": {
            "widget": MediaInputWidget(is_required=True),
            "validators": [
                MediaValidator(
                    media_types=IMAGE_TYPES,
                    max_size=MAX_IMAGE_SIZE_MB,
                    is_required=True,
                )
            ],
            "description": IMG_REQ % PREVIEW_PHOTO_RES,
        },
        "content": {
            "description": IMG_REQ % CONTENT_PHOTO_RES,
        },
    }

    form_ajax_refs = {
        "category": {
            "fields": ("name",),
            "order_by": "id",
        },
        "location": {
            "fields": ("name",),
            "order_by": "name",
        },
    }

    async def after_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        if not is_created:
            await invalidate_cache_partial(["get_news"])
            await invalidate_cache("get_one_news", model.id)
        await invalidate_cache_partial(["get_news"])
        return await super().after_model_change(data, model, is_created, request)

    async def after_model_delete(self, model: Any, request: Request) -> None:
        await invalidate_cache_partial(["get_news"])
        await invalidate_cache("get_one_news", model.id)
        return await super().after_model_delete(model, request)
