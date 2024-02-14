from typing import Any

from fastapi import Request
from sqladmin import ModelView
from wtforms import Form
from wtforms.validators import DataRequired

from src.admin.commons.formatters import (
    MediaFormatter,
    format_datetime,
    format_quill,
    format_array_of_string,
)
from src.admin.commons.utils import model_change_for_editor
from src.expedition.models import Expedition


class ExpeditionAdmin(ModelView, model=Expedition):
    is_async = True
    name_plural = "Експедиції"
    icon = "fa-solid fa-route"

    can_view_details = True
    can_export = False
    can_create = True

    column_list = form_columns = [
        Expedition.title,
        Expedition.short_description,
        Expedition.category,
        Expedition.location,
        Expedition.content,
        Expedition.expedition_date,
        Expedition.map_photo,
        Expedition.preview_photo,
        Expedition.authors,
        Expedition.editors,
        Expedition.photographers,
        Expedition.recording,
    ]
    column_labels = {
        Expedition.title: "Назва",
        Expedition.short_description: "Короткий опис",
        Expedition.map_photo: "Фото карти",
        Expedition.preview_photo: "Фото прев'ю",
        Expedition.expedition_date: "Дата експедиції",
        Expedition.content: "Контент",
        Expedition.category: "Категорія",
        Expedition.location: "Локація",
        Expedition.authors: "Збирачі",
        Expedition.editors: "Редактор",
        Expedition.photographers: "Відео-монтаж",
        Expedition.recording: "Запис",
    }
    column_details_exclude_list = [
        Expedition.id,
        Expedition.category_id,
        Expedition.city_id,
    ]
    column_formatters = {
        Expedition.content: format_quill,
        Expedition.authors: format_array_of_string,
        Expedition.editors: format_array_of_string,
        Expedition.photographers: format_array_of_string,
        Expedition.recording: format_array_of_string,
        Expedition.map_photo: MediaFormatter(),
        Expedition.preview_photo: MediaFormatter(),
    }
    form_args = {
        "category": {"validators": [DataRequired(message="Це поле обов'язкове")]},
        "location": {"validators": [DataRequired(message="Це поле обов'язкове")]},
        "expedition_date": {
            "validators": [DataRequired(message="Це поле обов'язкове")]
        },
        "content": {"validators": [DataRequired(message="Це поле обов'язкове")]},
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
        await model_change_for_editor(data, model, field_name="content")
        return await super().on_model_change(data, model, is_created, request)
