from typing import Any

from fastapi import Request
from sqladmin import ModelView
from wtforms import Form
from src.admin.commons.base import BaseAdmin

from src.admin.commons.formatters import (
    MediaFormatter,
    TextFormatter,
    format_date,
    format_quill,
    format_array_of_string,
)
from src.admin.commons.utils import (
    CustomSelect2TagsField,
    on_model_delete_for_quill,
    scaffold_form_for_quill,
)
from src.admin.commons.validators import QuillValidator
from src.news.models import News
from src.our_team.models import OurTeam

MODEL_TEAM_FIELDS = ["authors", "editors", "photographers"]


class NewsAdmin(BaseAdmin, model=News):
    name_plural = "Новини"
    icon = "fa-solid fa-kiwi-bird"

    column_list = [
        News.title,
        News.content,
        News.slider_caption,
        News.authors,
        News.editors,
        News.photographers,
        News.preview_photo,
        News.location,
        News.category,
        News.created_at,
    ]
    column_labels = {
        News.title: "Заголовок",
        News.content: "Контент",
        News.slider_caption: "Підпис до слайдера",
        News.authors: "Автори",
        News.editors: "Редактори",
        News.photographers: "Світлини",
        News.preview_photo: "Фото прев'ю",
        News.location: "Розташування",
        News.category: "Категорія",
        News.created_at: "Дата публікації",
    }

    form_columns = column_details_list = [
        News.title,
        News.preview_photo,
        News.authors,
        News.editors,
        News.photographers,
        News.location,
        News.category,
        News.created_at,
        News.content,
        News.slider_caption,
    ]

    column_formatters = {
        News.title: TextFormatter(text_align="left"),
        News.created_at: format_date,
        News.content: format_quill,
        News.authors: format_array_of_string,
        News.editors: format_array_of_string,
        News.photographers: format_array_of_string,
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
        "content": {"validators": [QuillValidator()]},
        **{field: {"model": OurTeam} for field in MODEL_TEAM_FIELDS},
    }
    form_ajax_refs = {
        "category": {
            "fields": ("name",),
            "order_by": "id",
        },
    }
