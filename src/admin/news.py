from typing import Any
from fastapi import Request
from wtforms.validators import DataRequired

from src.admin.commons.base import BaseAdmin
from src.admin.commons.formatters import (
    MediaFormatter,
    TextFormatter,
    format_date,
    format_quill,
    ArrayFormatter,
)
from src.admin.commons.utils import CustomSelect2TagsField, MediaInputWidget
from src.admin.commons.validators import MediaValidator
from src.database.redis import invalidate_cache, invalidate_cache_partial
from src.news.models import News
from src.our_team.models import OurTeam

MODEL_TEAM_FIELDS = ["authors", "editors", "photographers"]


class NewsAdmin(BaseAdmin, model=News):
    name_plural = "Новини"
    icon = "fa-solid fa-kiwi-bird"
    save_as = True

    column_labels = {
        News.title: "Заголовок",
        News.content: "Контент",
        News.short_description: "Короткий опис",
        News.authors: "Автори",
        News.editors: "Редактори",
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
    column_default_sort = ("created_at", True)
    form_columns = column_details_list = [
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
        "location": {"validators": [DataRequired()]},
        "category": {"validators": [DataRequired()]},
        **{field: {"model": OurTeam} for field in MODEL_TEAM_FIELDS},
        "preview_photo": {
            "validators": [MediaValidator(is_required=True)],
            "widget": MediaInputWidget(is_required=True),
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
