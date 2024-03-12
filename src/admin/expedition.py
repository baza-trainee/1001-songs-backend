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
from src.expedition.models import Expedition
from src.our_team.models import OurTeam

PREVIEW_PHOTO_RES = (300, 180)
MAP_PHOTO_RES = (460, 300)
CONTENT_PHOTO_RES = (1780, 1090)
MODEL_TEAM_FIELDS = ["authors", "editors", "photographers", "recording"]


class ExpeditionAdmin(BaseAdmin, model=Expedition):
    name_plural = "Експедиції"
    icon = "fa-solid fa-route"

    save_as = True

    column_labels = {
        Expedition.title: "Заголовок",
        Expedition.short_description: "Короткий опис",
        Expedition.map_photo: "Карта",
        Expedition.preview_photo: "Прев'ю",
        Expedition.expedition_date: "Дата",
        Expedition.content: "Контент",
        Expedition.category: "Категорія",
        Expedition.location: "Розташування",
        Expedition.authors: "Збирачі",
        Expedition.editors: "Редактор",
        Expedition.photographers: "Відео-монтаж",
        Expedition.recording: "Запис",
    }

    column_list = [
        Expedition.title,
        Expedition.content,
        Expedition.short_description,
        Expedition.preview_photo,
        Expedition.map_photo,
        Expedition.location,
        Expedition.expedition_date,
        Expedition.category,
        Expedition.authors,
        Expedition.editors,
        Expedition.photographers,
        Expedition.recording,
    ]
    form_columns = [
        Expedition.title,
        Expedition.short_description,
        Expedition.preview_photo,
        Expedition.location,
        Expedition.expedition_date,
        Expedition.map_photo,
        Expedition.category,
        Expedition.authors,
        Expedition.editors,
        Expedition.photographers,
        Expedition.recording,
        Expedition.content,
    ]
    column_formatters = {
        Expedition.short_description: TextFormatter(text_align="left"),
        Expedition.content: format_quill,
        Expedition.authors: ArrayFormatter(),
        Expedition.editors: ArrayFormatter(),
        Expedition.photographers: ArrayFormatter(),
        Expedition.recording: ArrayFormatter(),
        Expedition.map_photo: MediaFormatter(),
        Expedition.preview_photo: MediaFormatter(),
        Expedition.expedition_date: format_date,
    }
    column_searchable_list = [
        Expedition.title,
        Expedition.short_description,
    ]
    column_sortable_list = [Expedition.expedition_date]
    column_default_sort = ("expedition_date", True)
    form_files_list = [
        Expedition.preview_photo,
        Expedition.map_photo,
    ]
    form_quill_list = [
        Expedition.content,
    ]
    form_overrides = {
        **{field: CustomSelect2TagsField for field in MODEL_TEAM_FIELDS},
    }
    form_args = {
        "authors": {"validators": [ArrayStringValidator()]},
        "editors": {"validators": [ArrayStringValidator()]},
        "photographers": {"validators": [ArrayStringValidator()]},
        "recording": {"validators": [ArrayStringValidator()]},
        "category": {"validators": [DataRequired()]},
        "location": {"validators": [DataRequired()]},
        "expedition_date": {"validators": [PastDateValidator()]},
        "map_photo": {
            "widget": MediaInputWidget(is_required=True),
            "validators": [
                MediaValidator(
                    media_types=IMAGE_TYPES,
                    max_size=MAX_IMAGE_SIZE_MB,
                    is_required=True,
                )
            ],
            "description": IMG_REQ % MAP_PHOTO_RES,
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
        **{field: {"model": OurTeam} for field in MODEL_TEAM_FIELDS},
    }

    form_ajax_refs = {
        "category": {
            "fields": ("title",),
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
            await invalidate_cache_partial(["get_expeditions_list_by_category"])
            await invalidate_cache("get_expedition", model.id)
        await invalidate_cache_partial(["get_expeditions_list_by_category"])
        return await super().after_model_change(data, model, is_created, request)

    async def after_model_delete(self, model: Any, request: Request) -> None:
        await invalidate_cache_partial(["get_expeditions_list_by_category"])
        await invalidate_cache("get_expedition", model.id)
        return await super().after_model_delete(model, request)
