from typing import Any

from fastapi import Request
from wtforms.validators import DataRequired

from src.admin.commons.base import BaseAdmin
from src.admin.commons.exceptions import IMG_REQ
from src.admin.commons.formatters import MediaFormatter, format_quill, ArrayFormatter
from src.admin.commons.utils import CustomSelect2TagsField, MediaInputWidget
from src.admin.commons.validators import (
    ArrayStringValidator,
    MediaValidator,
    PastDateValidator,
)
from src.config import MAX_IMAGE_SIZE_MB, IMAGE_TYPES
from src.database.redis import invalidate_cache, invalidate_cache_partial
from src.our_project.models import OurProject
from src.our_team.models import OurTeam

PREVIEW_PHOTO_RES = (300, 180)
CONTENT_PHOTO_RES = (1780, 1090)


class OurProjectAdmin(BaseAdmin, model=OurProject):
    name_plural = "Актуальні проєкти"
    icon = "fa-solid fa-hands-holding-circle"
    category = "Про проєкт"
    save_as = False

    column_labels = {
        OurProject.title: "Заголовок",
        OurProject.short_description: "Короткий опис",
        OurProject.location: "Локація",
        OurProject.content: "Контент",
        OurProject.project_date: "Дата",
        OurProject.preview_photo: "Прев'ю",
        OurProject.authors: "Автор",
        OurProject.editors: "Редактор",
        OurProject.photographers: "Світлини",
    }
    form_columns = [
        OurProject.title,
        OurProject.short_description,
        OurProject.preview_photo,
        OurProject.project_date,
        OurProject.location,
        OurProject.authors,
        OurProject.editors,
        OurProject.photographers,
        OurProject.content,
    ]
    column_list = [
        OurProject.content,
        OurProject.title,
        OurProject.location,
        OurProject.project_date,
        OurProject.short_description,
        OurProject.preview_photo,
        OurProject.authors,
        OurProject.editors,
        OurProject.photographers,
    ]

    column_formatters = {
        OurProject.content: format_quill,
        OurProject.authors: ArrayFormatter(),
        OurProject.editors: ArrayFormatter(),
        OurProject.photographers: ArrayFormatter(),
        OurProject.preview_photo: MediaFormatter(),
    }
    form_quill_list = [
        OurProject.content,
    ]
    form_files_list = [
        OurProject.preview_photo,
    ]
    column_searchable_list = [
        OurProject.title,
        OurProject.short_description,
    ]
    column_sortable_list = [
        OurProject.project_date,
    ]
    form_overrides = {
        "authors": CustomSelect2TagsField,
        "editors": CustomSelect2TagsField,
        "photographers": CustomSelect2TagsField,
    }
    form_args = {
        "authors": {
            "model": OurTeam,
            "validators": [DataRequired(), ArrayStringValidator()],
        },
        "editors": {
            "model": OurTeam,
            "validators": [ArrayStringValidator()],
        },
        "photographers": {
            "model": OurTeam,
            "validators": [ArrayStringValidator()],
        },
        "location": {"validators": [DataRequired()]},
        "project_date": {"validators": [PastDateValidator()]},
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
        "location": {
            "fields": ("name",),
            "order_by": "name",
        },
    }

    async def after_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        if not is_created:
            await invalidate_cache_partial(["get_all_projects"])
            await invalidate_cache("get_project", model.id)
        await invalidate_cache_partial(["get_all_projects"])
        return await super().after_model_change(data, model, is_created, request)

    async def after_model_delete(self, model: Any, request: Request) -> None:
        await invalidate_cache_partial(["get_all_projects"])
        await invalidate_cache("get_project", model.id)
        return await super().after_model_delete(model, request)
